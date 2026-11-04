import requests

from Lab4.Model.dossier_modeles.ticket import Ticket

class ClientAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_users(self):
        try:
            reponse = requests.get(f"{self.base_url}/users/", timeout=10)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as erreur:
            print(f"Erreur API : {erreur}")
            return None

    def get_admins(self):
        try:
            reponse = requests.get(f"{self.base_url}/admins", timeout=10)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestExeption as erreur:
            print(f"Erreur API : {erreur}")
            return None

    def get_user(self, user_id : int):
        try:
            reponse = requests.get(f"{self.base_url}/user/{user_id}", timeout = 10)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as erreur:
            print(f"Erreur API : {erreur}")
            return None

    def get_tickets(self):
        try:
            reponse = requests.get(f"{self.base_url}/tickets/", timeout=10)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as erreur:
            print(f"Erreur API : {erreur}")
            return None

    def get_ticket(self, ticket_id :int):
        try:
            reponse = requests.get(f"{self.base_url}/tickets/{ticket_id}", timeout = 10)
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as erreur:
            print(f"Erreur API : {erreur}")
            return None

    def modif_ticket(self, ticket_id : int, ticket : Ticket):
        try:
            reponse = requests.put(f"{self.base_url}/tickets/{ticket_id}",
                json = {
                    "title" : ticket.title,
                    "description_ini" : ticket.description_ini,
                    "list_description" : [description.to_json() for description in ticket.list_description],
                    "status" : ticket.status,
                    "priority" : ticket.priority,
                    "user_assign" : ticket.user_assign,
                },
                timeout = 10
            )
            reponse.raise_for_status()
            return reponse.json()
        except requests.RequestException as erreur:
            print(f"Erreur API : {erreur}")
            return None

    
