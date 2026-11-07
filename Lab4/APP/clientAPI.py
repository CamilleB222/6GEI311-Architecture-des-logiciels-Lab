import base64
from datetime import datetime

import requests

from dossier_modeles.descriptionTicket.descriptionTicket import DescriptionTicket
from dossier_modeles.descriptionTicket.descriptionTicketImage import DescriptionTicketImage
from dossier_modeles.descriptionTicket.descriptionTicketTexte import DescriptionTicketTexte
from dossier_modeles.ticket.ticket import Ticket
from dossier_modeles.user.admin import Admin
from dossier_modeles.user.user import User
from dossier_modeles.statutTicket import StatutTicket

class ClientAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    def connect_user(self, name : str, mdp : str):
        try:
            reponse = requests.post(f"{self.base_url}/connect/", json={"name": name, "password": mdp}, timeout=10)
            reponse.raise_for_status()
            data = reponse.json()
            token : str = data.get("token")
            user_data = data.get("user")
            if user_data.get("role") == "admin":
                user_connected = Admin(
                    user_data.get("id"),
                    user_data.get("name"),
                    user_data.get("email")
                )
                #user_connected.json_to_user(user_data)
                return user_connected, token
            else:
                user_connected = User(
                    user_data.get("id"),
                    user_data.get("name"),
                    user_data.get("email"),
                    user_data.get("role")
                )
                #user_connected.json_to_user(user_data)
                return user_connected, token    
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def disconnect_user(self, token : str):
        try:
            reponse = requests.post(f"{self.base_url}/disconnect/", json={"token": token}, timeout=10)
            reponse.raise_for_status()
            if reponse.status_code == 200:
                return True
            else :
                return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False
    
    def get_users(self, token : str):
        try:
            reponse = requests.get(f"{self.base_url}/users/",headers={"X-Token": token}, timeout=10)
            reponse.raise_for_status()
            list_users : list[User] = self.json_to_users(reponse.json())
            return list_users
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def get_user(self, user_id : int, token : str):
        try:
            reponse = requests.get(f"{self.base_url}/user/{user_id}", headers={"X-Token": token}, timeout = 10)
            reponse.raise_for_status()
            user : User = self.json_to_user(reponse.json())
            return user
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def get_user_assign_tickets(self, user_id : int, token : str):
        try:
            reponse = requests.get(f"{self.base_url}/user/{user_id}/tickets", headers={"X-Token": token}, timeout = 10)
            reponse.raise_for_status()
            list_tickets : list[Ticket] = self.json_to_tickets(reponse.json())
            return list_tickets
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def get_admins(self , token : str):
        try:
            reponse = requests.get(f"{self.base_url}/admins", headers={"X-Token": token}, timeout=10)
            reponse.raise_for_status()
            list_admins : list[Admin] = self.json_to_admins(reponse.json())
            return list_admins
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def get_admin(self, admin_id : int, token : str):
        try:
            reponse = requests.get(f"{self.base_url}/admin/{admin_id}", headers={"X-Token": token}, timeout = 10)
            reponse.raise_for_status()
            admin : Admin = self.json_to_admin(reponse.json())
            return admin 
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None


    def get_tickets(self, token : str):
        try:
            reponse = requests.get(f"{self.base_url}/tickets/", headers={"X-Token": token}, timeout=10)
            reponse.raise_for_status()
            list_tickets : list[Ticket] = self.json_to_tickets(reponse.json())
            return list_tickets
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def create_tickets(self, titre : str, description_ini : str, priority : str, list_description : list[DescriptionTicket], token : str):
        try:
            reponse = requests.post(f"{self.base_url}/tickets/", 
                json = {
                    "title" : titre,
                    "description_initiale" : description_ini,
                    "priority" : priority,
                },
                headers={"X-Token": token},
                timeout=10
            )
            reponse.raise_for_status()
            ticket_id : int = reponse.json().get("ticket_id")
            for description in list_description:
                if not self.create_description_ticket(token, ticket_id, description):
                    print(f"Erreur lors de l'ajout de la description pour le ticket {ticket_id}")
                    return False
            return True
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False

    def get_ticket(self, ticket_id :int, token : str):
        try:
            reponse = requests.get(f"{self.base_url}/ticket/{ticket_id}", headers={"X-Token": token}, timeout = 10)
            reponse.raise_for_status()
            ticket : Ticket = self.json_to_ticket(reponse.json())
            return ticket
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def update_ticket(self, token : str, ticket : Ticket, list_description_id_supp : list[int]):
        try:
            reponse = requests.put(f"{self.base_url}/ticket/{ticket.ticket_id}",
                json = {
                    "title" : ticket.title,
                    "description_ini" : ticket.description_ini,
                    "status" : ticket.status.value,
                    "priority" : ticket.priority,
                    "user_assign" : ticket.user_assign
                },
                headers={"X-Token": token},
                timeout = 10
            )
            reponse.raise_for_status()
            for description_id in list_description_id_supp:
                if not self.delete_description(token,ticket.ticket_id,description_id):
                    print(f"Erreur lors de la suppression de la description pour le ticket {ticket.ticket_id}")
                    return False
            for description in ticket.list_description:
                if description.id is None:
                    if not self.create_description_ticket(token,ticket.ticket_id, description):
                        print(f"Erreur lors de la création de la description pour le ticket {ticket.ticket_id}")
                        return False
                else:
                    if not self.update_description_ticket(token, ticket.ticket_id, description.id, description):
                        print(f"Erreur lors de la mise à jour de la description pour le ticket {ticket.ticket_id}")
                        return False
            return True
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False

    def delete_ticket(self, ticket_id : int, token : str):
        try:
            reponse = requests.delete(f"{self.base_url}/ticket/{ticket_id}", headers={"X-Token": token}, timeout = 10)
            reponse.raise_for_status()
            return True
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False

    def assign_ticket(self, token : str, ticket_id : int, user_id : int):
        try:
            reponse = requests.post(f"{self.base_url}/ticket/{ticket_id}/assign", headers={"X-Token":token},
                json = {"user_id" : user_id},
                timeout = 10
            )
            reponse.raise_for_status()
            return True
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False
        
    def get_descriptions_ticket(self, token : str, ticket_id : int):
        try:
            reponse = requests.get(f"{self.base_url}/ticket/{ticket_id}/descriptions", headers={"X-Token":token}, timeout = 10)
            reponse.raise_for_status()
            list_description : list[DescriptionTicket] = self.json_to_descriptions(reponse.json())
            return list_description
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def create_description_ticket(self, token : str, ticket_id : int, description : DescriptionTicket):
        try:
            if isinstance(description, DescriptionTicketTexte):
                description_json = self.descriptionTexte_to_json(description)
            elif isinstance(description, DescriptionTicketImage):
                description_json = self.descriptionImage_to_json(description)
            else:
                raise ValueError("Type de description non supporté")
            
            reponse = requests.post(f"{self.base_url}/ticket/{ticket_id}/descriptions",
                json = description_json,
                headers = {"X-Token": token},
                timeout = 10
            )
            reponse.raise_for_status()
            return True
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False

    def get_description_ticket(self, token : str, ticket_id : int, description_id : int):
        try : 
            reponse = requests.get(f"{self.base_url}/ticket/{ticket_id}/description/{description_id}", headers = {"X-Token": token}, timeout = 10)
            reponse.raise_for_status()
            description : DescriptionTicket = self.json_to_description(reponse.json())
            return description
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return None
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return None

    def update_description_ticket(self, token : str, ticket_id : int, description_id : int, description : DescriptionTicket):
        try:
            if isinstance(description, DescriptionTicketTexte):
                description_json = self.descriptionTexte_to_json(description)
            elif isinstance(description, DescriptionTicketImage):
                description_json = self.descriptionImage_to_json(description)
            else:
                raise ValueError("Type de description non supporté")
            
            reponse = requests.put(f"{self.base_url}/ticket/{ticket_id}/description/{description_id}",
                json = description_json,
                headers = {"X-Token": token},
                timeout = 10
            )
            reponse.raise_for_status()
            return True
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False

    def delete_description(self, token : str, ticket_id : int, description_id : int):
        try:
            reponse = requests.delete(f"{self.base_url}/ticket/{ticket_id}/description/{description_id}", headers = {"X-Token": token}, timeout = 10)
            reponse.raise_for_status()
            return True
        except requests.HTTPError as erreur:
            print(f"Erreur HTTP : {erreur}")
            try:
                error_detail = reponse.json()
                print(f"Détails de l'erreur : {error_detail}")
            except ValueError:
                print("Impossible de décoder le JSON de l'erreur")
            return False
        except requests.RequestException as erreur:
            print(f"Erreur réseau : {erreur}")
            return False

    ###################################################################################################

    def json_to_user(self, json_data : dict) -> 'User':
        user_id : int = json_data.get("id")
        name : str = json_data.get("name")
        email : str = json_data.get("email")
        role : str = json_data.get("role")
        if role == "admin":
            return Admin(user_id, name, email, role)
        else:
            return User(user_id, name, email, role)
        
    def json_to_users(self,json_data : list[dict]) -> list['User']:
        users : list[User] = []
        for data in json_data:
            users.append(self.json_to_user(data))
        return users

    def json_to_admin(self, json_data : dict) -> 'Admin':
        admin_id : int = json_data.get("id")
        name : str = json_data.get("name")
        email : str = json_data.get("email")
        role : str = json_data.get("role")

        return Admin(admin_id, name, email, role)
            
    def json_to_admins(self,json_data : list[dict]) -> list['Admin']:
        admins : list[Admin] = []
        for data in json_data:
            admins.append(self.json_to_admin(data))
        return admins

    def json_to_ticket(self, json_data : dict) -> 'Ticket':
        ticket_id : int = json_data.get("ticket_id")
        title : str = json_data.get("title")
        description_ini : str = json_data.get("description_ini")
        list_description : list[DescriptionTicket] = self.json_to_descriptions(json_data.get("list_description"))
        status : str = StatutTicket(json_data.get("status"))
        priority : str = json_data.get("priority")
        creation_date_str : str = json_data.get("creation_date")
        creation_date: datetime = datetime.fromisoformat(creation_date_str) if creation_date_str else datetime.now()
        update_date_str : str = json_data.get("update_date")
        update_date: datetime = datetime.fromisoformat(update_date_str) if update_date_str else datetime.now()
        user_assign : str = json_data.get("user_assign")

        ticket = Ticket(ticket_id, title, description_ini, priority, creation_date, update_date, status, user_assign, list_description)
        return ticket


    def json_to_tickets(self, json_data : list[dict]) -> list['Ticket']:
        tickets : list[Ticket] = []
        for data in json_data:
            tickets.append(self.json_to_ticket(data))
        return tickets

    def descriptionTexte_to_json(self, description : DescriptionTicketTexte) -> dict:
        return {
            "type_description" : "texte",
            "titre" : description.get_titre(),
            "contenu" : description.get_description(),
            "binary_content" : ""
        }

    def json_to_description(self, json_data : dict) -> 'DescriptionTicket':
        description = None
        if json_data.get("type") == "texte":
            description : DescriptionTicketTexte = DescriptionTicketTexte(json_data.get("id"), json_data.get("titre"), json_data.get("description"))
        elif json_data.get("type") == "image":
            description : DescriptionTicketImage = DescriptionTicketImage(json_data.get("id"), json_data.get("titre"), json_data.get("filepath"), json_data.get("binary_content"))
        return description

    def json_to_descriptions(self, json_data : list[dict]) -> 'list[DescriptionTicket]':
        list_description : list[DescriptionTicket] = []
        for data in json_data:
            list_description.append(self.json_to_description(data))
        return list_description

    def descriptionImage_to_json(self, description : DescriptionTicketImage) -> dict:
        #with open(description.get_filepath(), "rb") as image_file:
        #    binary_content = base64.b64encode(image_file.read()).decode("utf-8")
        return {
            "type_description" : "image",
            "titre" : description.get_titre(),
            "contenu" : "",
            "binary_content" : description.get_binary_content()
        }
        
