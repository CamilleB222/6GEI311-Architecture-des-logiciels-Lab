from user import User
from admin import Admin
from ticket import Ticket
from datetime import datetime

list_user : list[User]
list_admin : list[Admin]
list_tickets : list[Ticket]

def main():
    admin1 = Admin(1, 'Camille Barrette', 'cbarrette@etu.uqac.ca',list_tickets)
    list_user.append(admin1)
    user1 = User(1,'Xavier Tremblay','xtremblay@etu.uqac.ca', 'développeur')
    user2 = User(2, 'Zachary Harvey', 'zharvey@etu.uqac.ca', 'apprenti')
    list_user.append(user1)
    list_user.append(user2)

    connexion : int
    connexion_reussi : bool = False
    deconnexion : bool = False
    action : int

    connexion = input("Connexion en tant que : \n 1 - Camille Barrette (admin)\n 2 - Xavier Tremblay (user) \n 3 - Zachary Harvey (user) \n Choix (numéro) : ")

    while not connexion_reussi:
        match connexion:
            case 1:
                while not deconnexion :
                    action = input("Quelle action voulez-vous faire:\n 1 - Assigner un ticket\n 2 - Fermer un ticket\n 3 - Voir tous les tickets 4 - Deconnexion\n Choix (numéro) : ")
                    match action:
                        case 1:
                            ticket_choisi : Ticket
                            nbr_valide : bool = False
                            ticket_existe : bool = False
                            ticket_asign : bool = False
                            while not ticket_asign:
                                while not ticket_existe:
                                    while not nbr_valide:
                                        try:
                                            ticket_id : int = int(input("Veuillez entrer l'ID du ticket à assigner : "))
                                            nbr_valide = True
                                        except ValueError:
                                            print("Erreur : Veillez entrer un nombre entier")
                                            nbr_valide = False

                                    
                                    ticket : Ticket
                                    for ticket in list_tickets:
                                        if ticket_id == ticket.ticket_id:
                                            ticket_choisi = ticket
                                            ticket_existe = True

                                    if not ticket_existe:
                                        print("Erreur : ID n'existe pas")

                                user_existe : bool = False
                                while not user_existe:
                                    user_name = input("Entrer le nom de l'utilisateur à qui assigner le ticket : ")

                                    user : User
                                    for user in list_user:
                                        if user_name == user.name:
                                            user_existe = True

                                    if not user_existe:
                                        print("Erreur : L'utilisateur n'existe pas")

                                admin1.assign_ticket(ticket_choisi,user_name)

                                if ticket_choisi.status == "ASSIGNÉ":
                                    print(f"Le ticket {ticket_id} à été assigné à {user_name}")
                                else:
                                    print("Erreur lors de l'assignement du ticket, veillez réessayer")

                        case 2:
                            ticket_choisi : Ticket
                            nbr_valide : bool = False
                            ticket_existe : bool = False
                            ticket_fermer : bool = False
                            while not ticket_fermer:
                                while not ticket_existe:
                                    while not nbr_valide:
                                        try:
                                            ticket_id : int = int(input("Veuillez entrer l'ID du ticket à fermer : "))
                                            nbr_valide = True
                                        except ValueError:
                                            print("Erreur : Veillez entrer un nombre entier")
                                            nbr_valide = False

                                    ticket : Ticket
                                    for ticket in list_tickets:
                                        if ticket_id == ticket.ticket_id:
                                            ticket_choisi = ticket
                                            ticket_existe = True

                                    if not ticket_existe:
                                        print("Erreur : ID n'existe pas")

                                    admin1.close_ticket(ticket_choisi)

                                    if ticket_choisi.status == "FERMER":
                                        print("Fermeture du ticket réussi")
                                        ticket_fermer = True
                                    else:
                                        print("Erreur lors de la fermeture du ticket, veillez réessayer")

                        case 3:
                            list_tickets_admin : list[Ticket]
                            list_tickets_admin = admin1.view_all_tickets()
                            ticket : Ticket
                            print("Les tickets sont :")
                            for ticket in list_tickets_admin:
                                print (f"{ticket.ticket_id}   {ticket.title}")

                        case 4:
                            deconnexion = True
                        case _:
                            print("Erreur : Action non valide")
            case 2 | 3 :
                connect_user : User
                connect_user = list_user[connexion]
                while not deconnexion :
                    action = input("Quelle action voulez-vous faire:\n 1 - Créer un ticket\n 2 - Afficher un ticket\n 3 - Mettre a jour un ticket 4 - Deconnexion\n Choix (numéro) : ")
                    match action:
                        case 1:
                            ticket : Ticket
                            ticket_id : int = max(ticket.ticket_id for ticket in list_tickets) + 1
                            title : str = input("Titre :")
                            description : str = input("Description :")
                            priority : str = input("Prioriter :")

                            ticket = Ticket(ticket_id, title, description, priority, datetime.now(), datetime.now())
                            list_tickets.append(ticket)
                            connect_user.create_ticket(ticket)

                            print("Ticket créer avec succes")
                             
                        case 2:
                            ticket_string : str = "Choisisser un ticket :"
                            i : int = 0
                            ticket : Ticket
                            for ticket in connect_user.asign_tickets:
                                ticket_string += f"\n {i} - {ticket.title}"

                            while not nbr_valide:
                                try:
                                    i : int = int(input(ticket_string))
                                    nbr_valide = True
                                    ticket = connect_user.asign_tickets[i]

                                except:
                                    print("Erreur : Veillez choisir un ticket existant")
                                    nbr_valide = False

                            connect_user.view_ticket(ticket)
                            
                        case 3:
                            pass
                        case 4:
                            deconnexion = True
                        case _:
                            action = print("Erreur : Action non valide")
                pass
            case _:
                connexion = input("Erreur : Identifiant non valise \nConnexion en tant que : \n 1 - Camille Barrette (admin)\n 2 - Xavier Tremblay (user) \n 3 - Zachary Harvey (user) \n")



