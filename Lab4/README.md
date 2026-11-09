# Architecture des logiciels
## Rapport laboratoire 4

### Auteurs
- Camille Barrette
- Xavier Tremblay

### Utilisation du projet
Pour utiliser l'outil actuel de gestion de tickets, il faut lancer l'API avec la commande 'uv run uvicorn main:app --reload --port 8080' lorsqu'on se trouve au niveau du dossier API.

le fichier de config pour changer le base url se trouve dans le dossier APP (config.py)

Pour lancer les client, il faut être au niveau du dossier APP et exécuter le fichier 'app.py'.

Pour aller voir la documentation de l'API : http://localhost:8080/docs.

les utilisateur disponible sont :
- Camille Barrette (admin)
- Xavier Tremblay (user)
- Zachary Harvey (user)
n'importe quel mot de passe fonctionne

### Résumer des modifications
Nous avons commencer par regrouper les fichiers exstants dans 3 dossiers : 
- APP : Pour toutes les pages de l'application, le controleur des pages et app.py
- API : Nous y avons mis le ticketManager
- Model : Pour les fichiers qui devrons être utilisé par l'API et l'APP (user, admin, ticket, statutTicket, descriptionTicket, etc.)

grande modification apporté :
- APP : 
    - Nous avons ajouter un clientAPI qui s'occupe d'envoyé les requetes à l'API et de faire les conversions json. 
    - Dans le controleur, nous avons remplacer toutes les appels qui était fait au ticketManager pour qu'il soit fait au clientAPI.
    - Nous avons rajouter une variable token dans le controleur pour identifier l'utilisateur a l'API.
- API :
    - Nous avons fait des controleur pour admin, authentification, ticket et user pour définir et spécifier les routes.
    - Un dossier pour garder les images.
    - Des schémas (user, description, ticket, auth) pour le spécifier les réponses de l'API (ce qu'il va renvoyer)
    - Un ficher maopers pour convertir en objet en json.
    - Un fichier dependencies pour faire la vérifications du token.
- Model : 
    - Nous avons ajouter des id au descriptions pour facilité le suivis.
    - Nous avons ajouter une variable au description en image (binary_content) pour pouvoir passer les image sous forme binaire entre l'APP et l'API.

### Leçons apprise
Durant ce laboratoire, nous avons appris à bien construre un API en :
- Spécifiants les réssources (user, admin, ticket)
- Spécifiants les actions qui peuvent être fait sur chaque ressource
    - user : get
    - admin : get
    - ticket : create, get, update, delete
- Spécifier les routes, les arguments demandé et retourner (voir la documentation de l'API sur http://localhost:8080/docs)

