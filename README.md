# 🛒 Shopping Cart API + Frontend

![Architecture Diagram](https://github.com/user-attachments/assets/871b99d0-8e9d-47ea-bd8d-0e6be6b6f3d6)

This is a simple project that demonstrates how to build and containerize a FastAPI backend with a static frontend served by Nginx. It's designed for academic purposes and highlights a clear separation between API and static content.

---

## 📦 Tech Stack

- **FastAPI** – Python-based high-performance web framework (backend/API)
- **SQLite** – Lightweight embedded database
- **Nginx** – Serves the static frontend (`index.html`)
- **Docker & Docker Compose** – Container orchestration

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py           # FastAPI application
│   └── __pycache__/
├── carrinho.db           # SQLite database
├── index.html            # Static HTML page (served by Nginx)
├── nginx/
│   └── default.conf      # Nginx config file
├── Dockerfile            # Dockerfile for FastAPI
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
└── diagram.png           # Architecture diagram
```

---

## 🚀 How to Run Locally (with Docker Compose)

### 1. Clone the repository

```bash
git clone https://github.com/vinytacana/marketplace-restful.git
cd marketplace-restful
```

### 2. Build and start the containers

```bash
docker-compose up --build
```

### 3. Access the application

- Frontend: [http://localhost](http://localhost)
- API Docs: [http://localhost/api/docs](http://localhost/api/docs)

---

## ⚙️ API Endpoints

Example root endpoint (`GET /api/`)

All API documentation is available via the [Swagger UI](http://localhost/api/docs).

---

## 📝 Notes

- The `index.html` is served by Nginx at the root `/` path.
- All API endpoints are routed via `/api/*`.
- The SQLite database (`carrinho.db`) is located in the root and accessed by FastAPI.

---

## 📷 Screenshots & Extras

Feel free to add screenshots of your running app or database visualizations here.

---

## 📄 License

This project is licensed under the terms of the `LICENSE` file.

