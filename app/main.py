from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

DATABASE_URL = "sqlite:///./carrinho.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELOS

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    preco = Column(Float)
    image_url = Column(String, nullable=True)  # <-- novo campo

    itens = relationship("ItemCarrinho", back_populates="produto")


class ItemCarrinho(Base):
    __tablename__ = "carrinho"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)

    produto = relationship("Produto", back_populates="itens")


Base.metadata.create_all(bind=engine)

# DEPENDÊNCIA DO BANCO
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROTAS

@app.post("/produtos/")
def criar_produto(nome: str, preco: float, image_url: str = "", db: Session = Depends(get_db)):
    db_prod = Produto(nome=nome, preco=preco, image_url=image_url)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.get("/produtos/")
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return [
        {
            "id": p.id,
            "nome": p.nome,
            "preco": p.preco,
            "image_url": p.image_url
        } for p in produtos
    ]

@app.delete("/produtos/{produto_id}")
def listar_produtos(produto_id: int, db: Session = Depends(get_db)):
    item = db.query(Produto).filter(Produto.id == produto_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado ")
    db.delete(item)
    db.commit()
    return {"detail": "Item removido"}

@app.get("/carrinho/")
def ver_carrinho(db: Session = Depends(get_db)):
    itens = db.query(ItemCarrinho).all()
    return [
        {
            "produto": item.produto.nome,
            "preco_unitario": item.produto.preco,
            "quantidade": item.quantidade,
            "total": item.produto.preco * item.quantidade,
            "image_url": item.produto.image_url
        }
        for item in itens
    ]

@app.post("/carrinho/")
def adicionar_ao_carrinho(produto_id: int, quantidade: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    item = db.query(ItemCarrinho).filter(ItemCarrinho.produto_id == produto_id).first()
    if item:
        item.quantidade += quantidade
    else:
        item = ItemCarrinho(produto_id=produto_id, quantidade=quantidade)
        db.add(item)

    db.commit()
    db.refresh(item)
    return item

@app.put("/carrinho/{produto_id}")
def atualizar_quantidade(produto_id: int, quantidade: int, db: Session = Depends(get_db)):
    item = db.query(ItemCarrinho).filter(ItemCarrinho.produto_id == produto_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")
    item.quantidade = quantidade
    db.commit()
    db.refresh(item)
    return item

@app.delete("/carrinho/{produto_id}")
def remover_item(produto_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemCarrinho).filter(ItemCarrinho.produto_id == produto_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")
    db.delete(item)
    db.commit()
    return {"detail": "Item removido do carrinho"}

