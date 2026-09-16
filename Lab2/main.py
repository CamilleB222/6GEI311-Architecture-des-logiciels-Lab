from user import User
from admin import Admin
from ticket import Ticket

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
                    match ation:
                        case 1:
                            nbr_valide : bool = False
                            while not nbr_valide:
                                try:
                                    ticket_id : int = int(input("Veuillez entrer l'ID du ticket à assigner : "))
                                    nbr_valide = True
                                except ValueError:
                                    print("Erreur : Veillez entrer un nombre entier")
                                    nbr_valide = False

                            ticket_existe : bool = False
                            ticket : Ticket
                            for ticket in list_ticket:
                                if (ticket_id == ticket.ticket_id):
                                    ticket_existe = True

                            if (not ticket_existe):
                                print("Erreur : ID ")

                        case 2:
                            pass
                        case 3:
                            pass
                        case 4:
                            pass
                        case _:
                            print("Erreur : Action non valide")
            case 2 | 3 :
                pass

            case _:
                connexion = input("Erreur : Identifiant non valise \nConnexion en tant que : \n 1 - Camille Barrette (admin)\n 2 - Xavier Tremblay (user) \n 3 - Zachary Harvey (user) \n")



