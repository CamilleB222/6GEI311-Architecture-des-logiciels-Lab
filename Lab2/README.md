# Architecture des logiciels
## Rapport laboratoire 2

### Auteurs
- Camille Barrette
- Xavier Tremblay

### 1. Utilisation du projet
Pour utiliser l'outil actuel de gestion de tickets, il faut exécuter le fichier `main.py`.

### 2. Concepts appris et bonnes pratiques
Dans ce laboratoire, nous avons appris à utiliser plusieurs bonnes pratiques de conception logicielle, notamment :

- Le contrôleur avec la classe `TicketManager`
- Le patron stratégie avec l'interface `DescriptionTicket`, qui permet d'ajouter facilement de nouveaux types de description, comme `DescriptionTicketImage` et `DescriptionTicketTexte`
- Le patron créateur, puisque les tickets sont composés de descriptions de ticket et que la classe `Ticket` s'occupe de créer ces objets `DescriptionTicket`

### 3. Modifications apportées au diagramme de classes
Le nouveau diagramme de classes se trouve dans le dossier `diagramme` du projet. Plusieurs changements y ont été apportés.

#### Nouvelles classes
- `TicketManager` : sert de contrôleur et fait le lien entre l'utilisateur et le reste du code. Il appelle les fonctions nécessaires selon les demandes de l'utilisateur. Il contient notamment la liste complète des tickets ainsi que la liste des utilisateurs pour l'assignation. Ses méthodes incluent : `view_all_ticket`, `creat_ticket`, `view_ticket`, `update_ticket`, `assign_ticket` et `close_ticket`.
- `DescriptionTicket` : une interface pour les différents types de description.
- `DescriptionTicketTexte` : pour les descriptions sous forme de texte.
- `DescriptionTicketImage` : pour les descriptions sous forme d'image.
- `TicketStatut` : une classe `enum` pour les différents états possibles des tickets.

#### Modifications des classes existantes
- `User`
  - En plus des quatre attributs déjà présents, on a ajouté une liste des tickets qui lui sont assignés ainsi qu'une liste des tickets qu'il a créés.
- `Admin`
  - Il hérite maintenant de la classe `User`; il peut donc aussi créer, voir et mettre à jour des tickets.
  - Il ne possède plus la méthode pour voir tous les tickets, car cette responsabilité est maintenant gérée par `TicketManager`.
- `Ticket`
  - Au lieu que `description` soit une chaîne de caractères, elle est maintenant une liste de `DescriptionTicket`.
  - `Status` n'est plus une chaîne de caractères, mais un `TicketStatut`.
  - Ajout d'un attribut contenant une liste de commentaires.
  - Ajout de la méthode `addDescription`.

---

Ce README résume les concepts et les changements effectués dans le laboratoire 2.