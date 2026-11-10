# API/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importation des routeurs depuis le dossier controllers
from controllers.auth_controller import router as auth_router
from controllers.user_controller import router as user_controller
from controllers.admin_controller import router as admin_controller
from controllers.ticket_controller import router as ticket_controller

#Classe métier
from dossier_modeles import Admin, Ticket, User
from program_list import list_admin, list_user, list_tickets
from datetime import datetime

#Définir les valeurs par défaut
def register_user(user : User):
    if isinstance(user, Admin):
        if user not in list_admin:
            list_admin.append(user)
    else:
        if user not in list_user:
            list_user.append(user)


admin1 = Admin(1, 'Camille Barrette', 'cbarrette@etu.uqac.ca')
register_user(admin1)
user1 = User(1,'Xavier Tremblay','xtremblay@etu.uqac.ca', 'développeur')
user2 = User(2, 'Zachary Harvey', 'zharvey@etu.uqac.ca', 'apprenti')
register_user(user1)
register_user(user2)

#Pour les test
c =  Ticket(1,"c","c","c",datetime.now(), datetime.now())
c1 = Ticket(2,"c1","c1","c1",datetime.now(), datetime.now())
c2 = Ticket(3,"c2","c2","c2",datetime.now(), datetime.now())
c3 = Ticket(4,"c3","c3","c3",datetime.now(), datetime.now())
c4 = Ticket(5,"c4","c4","c4",datetime.now(), datetime.now())

list_tickets.append(c)
list_tickets.append(c1)
list_tickets.append(c2)
list_tickets.append(c3)
list_tickets.append(c4)

admin1.create_ticket(c)
admin1.create_ticket(c1)
admin1.create_ticket(c2)
admin1.create_ticket(c3)
admin1.create_ticket(c4)


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
app.include_router(user_controller)
app.include_router(admin_controller)
app.include_router(ticket_controller)

# Route racine optionnelle pour tester l'état du serveur
@app.get("/", tags=["Health Check"])
def root():
    return {"status": "ok", "message": "L'API est opérationnelle"}

# Démarer l'API
#uv run uvicorn main:app --reload --port 8080

#Aller voir la documentation
#http://localhost:8080/docs