# API/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importation des routeurs depuis le dossier controllers
from controllers.auth_controller import router as auth_router

app = FastAPI(
    title="API de Gestion de Tickets",
    description="API REST MVC pour la gestion de tickets, utilisateurs et administrateurs",
    version="1.0.0"
)

# Configuration CORS (nécessaire si votre app PyQt6 ou un navigateur communique avec l'API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des contrôleurs (Routeurs)
app.include_router(auth_router)

# Route racine optionnelle pour tester l'état du serveur
@app.get("/", tags=["Health Check"])
def root():
    return {"status": "ok", "message": "L'API est opérationnelle"}

# Démarer l'API
#uv run uvicorn main:app --reload --port 8080

#Aller voir la documentation
#http://localhost:8080/docs