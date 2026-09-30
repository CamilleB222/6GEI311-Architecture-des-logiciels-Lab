from user import User
from admin import Admin
from ticket import Ticket
from datetime import datetime
from ticketManager import TicketManager
from statutTicket import StatutTicket
from descriptionTicketTexte import DescriptionTicketTexte
from descriptionTicketImage import DescriptionTicketImage
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

root = tk.Tk()
root.withdraw()

list_user : list[User] = list[User]()
list_admin : list[Admin] = list[Admin]()
list_tickets : list[Ticket] = list[Ticket]()
ticket_manager : TicketManager = TicketManager()

def register_user(user : User):
    if isinstance(user, Admin):
        if user not in list_admin:
            list_admin.append(user)
    else:
        if user not in list_user:
            list_user.append(user)

    ticket_manager.register_user(user)

def get_ticket_by_id() -> Ticket | None:
    ticket_choisi : Ticket | None
    ticket_existe : bool = False

    while not ticket_existe:
        nbr_valide : bool = False
        while not nbr_valide:
            try:
                ticket_id : int = int(input("\nVeuillez entrer l'ID du ticket (Entrez 0 pour quitter) : "))
                nbr_valide = True
            except ValueError:
                print("\nErreur : Veillez entrer un nombre entier")
                nbr_valide = False

        if ticket_id != 0:
            ticket : Ticket
            for ticket in ticket_manager.view_all_ticket():
                if ticket_id == ticket.ticket_id:
                    ticket_choisi = ticket
                    ticket_existe = True

            if not ticket_existe:
                print("\nErreur : ID n'existe pas")
        else:
            ticket_choisi = None
            ticket_existe = True

    return ticket_choisi
    
def assigner_ticket(connect_admin : Admin):
    if len(ticket_manager.view_all_ticket()) == 0:
        print("\nAucun ticket n'existe")
        return 

    ticket_choisi : Ticket
    ticket_asign : bool = False
    while not ticket_asign:
        ticket_choisi = get_ticket_by_id()

        if ticket_choisi is not None:
            user_existe : bool = False
            user_choisi : User | None

            while not user_existe:
                user_name = input("\nEntrer le nom de l'utilisateur à qui assigner le ticket (Entrez 0 pour quitter) : ")

                if user_name != "0":
                    user : User
                    for user in list_user:
                        if user_name == user.name:
                            user_existe = True
                            user_choisi = user
                else:
                    user_existe = True
                    user_choisi = None

                if not user_existe:
                    print("\nErreur : L'utilisateur n'existe pas")

            if user_choisi is not None :
                ticket_manager.assign_Ticket(connect_admin, user_choisi, ticket_choisi)

                if ticket_choisi.status == StatutTicket.ASSIGNÉ:
                    print(f"\nLe ticket {ticket_choisi.ticket_id} à été assigné à {user_name}")
                    ticket_asign = True
                else:
                    print("\nErreur lors de l'assignement du ticket, veillez réessayer")
            else:
                ticket_asign = True
        else:
            ticket_asign = True

def fermer_ticket(connect_admin : Admin):
    if len(ticket_manager.view_all_ticket()) == 0:
        print("\nAucun ticket n'existe")
        return
    
    ticket_choisi : Ticket | None
    ticket_fermer : bool = False
    while not ticket_fermer:
        ticket_choisi = get_ticket_by_id()

        if ticket_choisi is not None:
            ticket_manager.close_ticket(connect_admin ,ticket_choisi)

            if ticket_choisi.status == StatutTicket.FERMER:
                print("\nFermeture du ticket réussi")
                ticket_fermer = True
            else:
                print("\nErreur lors de la fermeture du ticket, veillez réessayer")
        else:
            ticket_fermer = True

def voir_ticket():
    list_tickets_manager : list[Ticket]
    list_tickets_manager = ticket_manager.view_all_ticket()
    ticket : Ticket
    print("\nLes tickets sont :")
    for ticket in list_tickets_manager:
        print (f"{ticket.ticket_id}   {ticket.title}")

def creer_ticket(connect_user : User):
    ticket : Ticket
    ticket_id : int
    if not len(list_tickets) == 0:
        ticket_id = max(ticket.ticket_id for ticket in list_tickets) + 1
    else:
        ticket_id = 1

    title : str = input("\nTitre : ")
    description : str = input("Description : ")
    priority : str = input("Prioriter : ")

    ticket = Ticket(ticket_id, title, description, priority, datetime.now(), datetime.now())
    list_tickets.append(ticket)
    ticket_manager.creat_ticket(connect_user, ticket)

    ajouter_description : bool = True
    type_description : str
    while ajouter_description:
        type_description = input("\nVoulez-vous ajouter des descriptions sous forme de : \n 1 - texte \n 2 - image \n 3 - Ne pas ajouter d'autre description \n Choix (numéro) : ")
        if (type_description == "1"): #texte
            description_texte : str
            description_texte = input("Veillez écrire la description : ")
            ticket.add_description(DescriptionTicketTexte, description_texte)
            print("\nDescription (texte) ajouté avec succes")
        elif (type_description == "2"): #image
            description_image : str

            description_image = filedialog.askopenfilename(
                title = "Choisir une image",
                initialdir=Path.home
            )
            
            ticket.add_description(DescriptionTicketImage, description_image)
            print("\nDescription (image) ajouté avec succes")
        elif (type_description == "3"):
            ajouter_description = False
        else:
            print("Erreur : Veuillez entrer un nombre valide")
            
    print("\nTicket créer avec succès")

def afficher_ticket(connect_user : User):
    if len(connect_user.asign_tickets) == 0:
        print("\nAucun ticket présent dans votre liste de ticket")
        return

    ticket_string : str = "Choisisser un ticket (Entrez 0 pour quitter) :"
    nbr_tickets : int = 1
    ticket : Ticket | None
    for ticket in connect_user.asign_tickets:
        ticket_string += f"\n {nbr_tickets} - {ticket.title}"
        nbr_tickets += 1

    ticket_string += "\n Choix (numéro) : "
        
    nbr_valide : bool = False 
    while not nbr_valide:
        try:
            i : int = int(input(ticket_string))
            nbr_valide = True
            if i != 0 :
                ticket = connect_user.asign_tickets[i - 1]
            else:
                ticket = None

        except:
            print("\nErreur : Veillez choisir un ticket existant")
            nbr_valide = False

    if ticket != 0:
        print(ticket_manager.view_ticket(connect_user, ticket))

def mise_a_jour_ticket(connect_user : User):
    if len(connect_user.asign_tickets) == 0:
        print("\nAucun ticket présent dans votre liste de ticket")
        return

    ticket_existe : bool = False
    nbr_valide : bool = False
    while not ticket_existe:
        nbr_valide = False
        while not nbr_valide:
            try:
                ticket_id : int = int(input("\nVeuillez entrer l'ID du ticket (Entrez 0 pour quitter) : "))
                nbr_valide = True
            except ValueError:
                print("\nErreur : Veillez entrer un nombre entier")
                nbr_valide = False

        if ticket_id != 0:
            ticket : Ticket
            for ticket in connect_user.asign_tickets:
                if ticket_id == ticket.ticket_id:
                    ticket_choisi = ticket
                    ticket_existe = True

            if not ticket_existe:
                print("\nErreur : ID n'existe pas")
            else:
                status_ticket = ticket_choisi.status
                ticket_manager.update_ticket(connect_user, ticket_choisi)
                if status_ticket != ticket_choisi.status:
                    print(f"\nMise à jout du ticket {ticket_choisi.ticket_id} réussi")
                else:
                    print("\nErreur : Ticket non mis à jour")
        else:
            ticket_existe = True
        


def main():
    
    admin1 = Admin(1, 'Camille Barrette', 'cbarrette@etu.uqac.ca')
    register_user(admin1)
    user1 = User(1,'Xavier Tremblay','xtremblay@etu.uqac.ca', 'développeur')
    user2 = User(2, 'Zachary Harvey', 'zharvey@etu.uqac.ca', 'apprenti')
    register_user(user1)
    register_user(user2)

    connexion : str
    connexion_reussi : bool = False
    deconnexion : bool = False
    action : int


    while not connexion_reussi:
        deconnexion = False
        connexion = input("\nConnexion en tant que : \n 1 - Camille Barrette (admin)\n 2 - Xavier Tremblay (user) \n 3 - Zachary Harvey (user) \n Choix (numéro) : ")
        match connexion:
            case '1': #Admin
                connect_admin : Admin = list_admin[int(connexion) - 1]
                while not deconnexion :
                    action = input("\nQuelle action voulez-vous faire:\n 1 - Assigner un ticket\n 2 - Fermer un ticket\n 3 - Voir tous les tickets\n 4 - Créer un ticket\n 5 - Afficher un ticket\n 6 - Mettre a jour un ticket\n 7 - Deconnexion\n Choix (numéro) : ")
                    match action:
                        case '1': #Assigner ticket
                            assigner_ticket(connect_admin)

                        case '2': #Fermer ticket
                            fermer_ticket(connect_admin)

                        case '3': #Voir tous les tickets
                            voir_ticket()

                        case '4': #Créer un ticket
                            creer_ticket(connect_admin)
                             
                        case '5': #Afficher un ticket
                            afficher_ticket(connect_admin)
                            
                        case '6': #Mettre à jout un ticket
                            mise_a_jour_ticket(connect_admin)

                        case '7': #Deconnexion
                            deconnexion = True
                        case _:
                            print("\nErreur : Action non valide")
            case '2' | '3' : #User
                connect_user : User
                connect_user = list_user[int(connexion) - 2]
                while not deconnexion :
                    action = input("\nQuelle action voulez-vous faire:\n 1 - Créer un ticket\n 2 - Afficher un ticket\n 3 - Mettre a jour un ticket\n 4 - Deconnexion\n Choix (numéro) : ")
                    match action:
                        case '1': #Créer un ticket
                            creer_ticket(connect_user)
                             
                        case '2': #Afficher un ticket
                            afficher_ticket(connect_user)
                            
                        case '3': #Mettre à jout un ticket
                            mise_a_jour_ticket(connect_user)

                        case '4': #Deconnexion
                            deconnexion = True
                        case _:
                            action = print("\nErreur : Action non valide")
        
            case _:
                print("\nErreur : Identifiant non valise")

if __name__ == "__main__":
    main()