from fastapi import FastAPI
from dossier_modeles import Ticket, User, Admin

app = FastAPI(title="MVC FastAPI Example")
#app.include_router(user_router)

