from user import User
from admin import Admin
from ticket import Ticket
from datetime import datetime

list_user : list[User] = list[User]()
list_admin : list[Admin] = list[Admin]()
list_tickets : list[Ticket] = list[Ticket]()

def main():
    admin1 = Admin(1, 'Camille Barrette', 'cbarrette@etu.uqac.ca',list_tickets)
    list_admin.append(admin1)
    user1 = User(1,'Xavier Tremblay','xtremblay@etu.uqac.ca', 'développeur')
    user2 = User(2, 'Zachary Harvey', 'zharvey@etu.uqac.ca', 'apprenti')
    list_user.append(user1)
    list_user.append(user2)

    connexion : str
    connexion_reussi : bool = False
    deconnexion : bool = False
    action : int


    while not connexion_reussi:
        deconnexion = False
        connexion = input("\nConnexion en tant que : \n 1 - Camille Barrette (admin)\n 2 - Xavier Tremblay (user) \n 3 - Zachary Harvey (user) \n Choix (numéro) : ")
        match connexion:
            case '1':
                while not deconnexion :
                    action = input("\nQuelle action voulez-vous faire:\n 1 - Assigner un ticket\n 2 - Fermer un ticket\n 3 - Voir tous les tickets\n 4 - Deconnexion\n Choix (numéro) : ")
                    match action:
                        case '1':
                            if len(admin1.view_all_tickets()) !=0:
                                ticket_choisi : Ticket
                                nbr_valide : bool = False
                                ticket_existe : bool = False
                                ticket_asign : bool = False
                                while not ticket_asign:
                                    while not ticket_existe:
                                        nbr_valide = False
                                        while not nbr_valide:
                                            try:
                                                ticket_id : int = int(input("\nVeuillez entrer l'ID du ticket à assigner : "))
                                                nbr_valide = True
                                            except ValueError:
                                                print("\nErreur : Veillez entrer un nombre entier")
                                                nbr_valide = False

                                        
                                        ticket : Ticket
                                        for ticket in list_tickets:
                                            if ticket_id == ticket.ticket_id:
                                                ticket_choisi = ticket
                                                ticket_existe = True

                                        if not ticket_existe:
                                            print("\nErreur : ID n'existe pas")


                                    user_existe : bool = False
                                    while not user_existe:
                                        user_name = input("\nEntrer le nom de l'utilisateur à qui assigner le ticket : ")

                                        user : User
                                        user_choisi : User
                                        for user in list_user:
                                            if user_name == user.name:
                                                user_existe = True
                                                user_choisi = user

                                        if not user_existe:
                                            print("\nErreur : L'utilisateur n'existe pas")

                                    admin1.assign_ticket(ticket_choisi,user_choisi)

                                    if ticket_choisi.status == "ASSIGNÉ":
                                        print(f"\nLe ticket {ticket_id} à été assigné à {user_name}")
                                        ticket_asign = True
                                    else:
                                        print("\nErreur lors de l'assignement du ticket, veillez réessayer")

                            else:
                                print("\nAucun ticket n'existe")

                        case '2':
                            if len(admin1.view_all_tickets()) !=0:
                                ticket_choisi : Ticket
                                nbr_valide : bool = False
                                ticket_existe : bool = False
                                ticket_fermer : bool = False
                                while not ticket_fermer:
                                    while not ticket_existe:
                                        nbr_valide = False
                                        while not nbr_valide:
                                            try:
                                                ticket_id : int = int(input("\nVeuillez entrer l'ID du ticket à fermer : "))
                                                nbr_valide = True
                                            except ValueError:
                                                print("\nErreur : Veillez entrer un nombre entier")
                                                nbr_valide = False

                                        ticket : Ticket
                                        for ticket in list_tickets:
                                            if ticket_id == ticket.ticket_id:
                                                ticket_choisi = ticket
                                                ticket_existe = True

                                        if not ticket_existe:
                                            print("\nErreur : ID n'existe pas")
                                        else:
                                            admin1.close_ticket(ticket_choisi)

                                            if ticket_choisi.status == "FERMER":
                                                print("\nFermeture du ticket réussi")
                                                ticket_fermer = True
                                            else:
                                                print("\nErreur lors de la fermeture du ticket, veillez réessayer")
                            else:
                                print("\nAucun ticket n'existe")

                        case '3':
                            list_tickets_admin : list[Ticket]
                            list_tickets_admin = admin1.view_all_tickets()
                            ticket : Ticket
                            print("\nLes tickets sont :")
                            for ticket in list_tickets_admin:
                                print (f"{ticket.ticket_id}   {ticket.title}")

                        case '4':
                            deconnexion = True
                        case _:
                            print("\nErreur : Action non valide")
            case '2' | '3' :
                connect_user : User
                connect_user = list_user[int(connexion) - 2]
                while not deconnexion :
                    action = input("\nQuelle action voulez-vous faire:\n 1 - Créer un ticket\n 2 - Afficher un ticket\n 3 - Mettre a jour un ticket\n 4 - Deconnexion\n Choix (numéro) : ")
                    match action:
                        case '1':
                            ticket : Ticket
                            ticket_id : int
                            if not len(list_tickets) == 0:
                                ticket_id = max(ticket.ticket_id for ticket in list_tickets) + 1
                            else:
                                ticket_id = 1

                            title : str = input("\nTitre :")
                            description : str = input("Description :")
                            priority : str = input("Prioriter :")

                            ticket = Ticket(ticket_id, title, description, priority, datetime.now(), datetime.now())
                            list_tickets.append(ticket)
                            connect_user.create_ticket(ticket)

                            print("\nTicket créer avec succes")
                             
                        case '2':

                            if len(connect_user.asign_tickets) != 0:

                                ticket_string : str = "Choisisser un ticket :"
                                i : int = 0
                                ticket : Ticket
                                for ticket in connect_user.asign_tickets:
                                    ticket_string += f"\n {i} - {ticket.title}"

                                ticket_string += "\n Choix (numéro) : "
                                    
                                nbr_valide : bool = False 
                                while not nbr_valide:
                                    try:
                                        i : int = int(input(ticket_string))
                                        nbr_valide = True
                                        ticket = connect_user.asign_tickets[i]

                                    except:
                                        print("\nErreur : Veillez choisir un ticket existant")
                                        nbr_valide = False

                                connect_user.view_ticket(ticket)
                            else:
                                print("\nAucun ticket présent dans votre liste de ticket")
                            
                        case '3':
                            if len(connect_user.asign_tickets) != 0:
                                ticket_existe : bool = False
                                nbr_valide : bool = False
                                while not ticket_existe:
                                    nbr_valide = False
                                    while not nbr_valide:
                                        try:
                                            ticket_id : int = int(input("\nVeuillez entrer l'ID du ticket à mettre à jour : "))
                                            nbr_valide = True
                                        except ValueError:
                                            print("\nErreur : Veillez entrer un nombre entier")
                                            nbr_valide = False

                                    ticket : Ticket
                                    for ticket in user_choisi.asign_tickets:
                                        if ticket_id == ticket.ticket_id:
                                            ticket_choisi = ticket
                                            ticket_existe = True

                                    if not ticket_existe:
                                        print("\nErreur : ID n'existe pas")
                                    else:
                                        status_ticket = ticket_choisi.status
                                        connect_user.update_ticket(ticket_choisi)
                                        if status_ticket != ticket_choisi.status:
                                            print(f"\nMise à jout du ticket {ticket_choisi.ticket_id} réussi")
                                        else:
                                            print("\nErreur : Ticket non mis à jour")

                            else:
                                print("\nAucun ticket présent dans votre liste de ticket")

                        case '4':
                            deconnexion = True
                        case _:
                            action = print("\nErreur : Action non valide")
        
            case _:
                print("\nErreur : Identifiant non valise")

if __name__ == "__main__":
    main()