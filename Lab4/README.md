# Architecture des logiciels
## Rapport laboratoire 4

### Auteurs
- Camille Barrette
- Xavier Tremblay

### Utilisation du projet
Pour utiliser l'outil actuel de gestion de tickets, il faut lancer l'API avec la commande 'uv run uvicorn main:app --host 0.0.0.0 --reload --port 8080' lorsqu'on se trouve au niveau du dossier API.

Le fichier de configuration pour changer le 'BASE_URL' se trouve dans le dossier APP (config.py)

Pour lancer les clients, il faut être au niveau du dossier APP et exécuter le fichier 'app.py'.

Pour aller voir la documentation de l'API : http://localhost:8080/docs.

les utilisateurs disponibles sont :
- Camille Barrette (admin)
- Xavier Tremblay (user)
- Zachary Harvey (user)
N'importe quel mot de passe fonctionne

### Résumer des modifications
Nous avons commencé par regrouper les fichiers existants dans trois dossiers : 
- APP : Pour toutes les pages de l'application, le controleur des pages et 'app.py'
- API : Nous y avons mis le ticketManager
- Model : Pour les fichiers qui devront être utilisés par l'API et l'APP (user, admin, ticket, statutTicket, descriptionTicket, etc.)

grande modification apporté :
- APP : 
    - Nous avons ajouté un clientAPI qui s'occupe d'envoyer les requêtes à l'API et de faire les conversions JSON. 
    - Dans le controleur, nous avons remplacé tous les appels qui étaient faits au ticketManager pour qu'il soient faits au clientAPI.
    - Nous avons ajouté une variable token dans le controleur pour identifier l'utilisateur auprès de l'API.
- API :
    - Nous avons fait des controleur pour admin, authentification, ticket et user pour définir et spécifier les routes.
    - Un dossier pour garder les images.
    - Des schémas (user, description, ticket, auth) pour spécifier les réponses de l'API (ce qu'elle va renvoyer)
    - Un ficher mappers pour convertir les objet en JSON.
    - Un fichier dependencies pour faire la vérifications du token.
- Model : 
    - Nous avons ajouté des id au descriptions pour faciliter le suivi.
    - Nous avons ajouté une variable au description en image (binary_content) pour pouvoir passer les images sous forme binaire entre l'APP et l'API.

### Leçons apprise
Durant ce laboratoire, nous avons appris à bien construire un API en :
- Spécifiant les ressources (user, admin, ticket)
- Spécifiant les actions qui peuvent être faites sur chaque ressource
    - user : get
    - admin : get
    - ticket : create, get, update, delete
- Spécifiant les routes, les arguments demandés et retournés (voir la documentation de l'API sur http://localhost:8080/docs)

