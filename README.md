# Créez une API sécurisée RESTful en utilisant Django REST

### Openclassroom projet 10
Le projet vise à développer une API Restful pour la société SoftDesk. Cette entreprise a l'intention de mettre en place cette API pour faciliter les échanges entre les divers acteurs d'une équipe de développement, permettant ainsi de discuter des défis techniques qu'ils rencontrent.

La conception de cette API doit se baser sur Django Rest Framework.

L'API doit respecter les lignes directrices suivantes :

Les utilisateurs doivent avoir la capacité de créer un compte et de se connecter.
Une authentification est nécessaire pour accéder globalement à l'API.
Seul le créateur d'un projet a le droit de le supprimer ou de le modifier, et donc d'ajouter des contributeurs.
Les contributeurs d'un projet ont un accès en lecture seule, mais ils peuvent créer des problèmes.
Les problèmes suivent une logique similaire à celle des projets : seuls les créateurs ont le droit de les mettre à jour ou de les supprimer.
Les problèmes peuvent faire l'objet de commentaires.

Le projet utilise le langage Python.

## Pré-requis:
   - Language de programmation:
      Python3
   - Module utilisés:
      - Django 4
   - Poetry

## Installation:
Clonez le dépôt du projet :
git clone <lien-du-depot>
cd OCR_projet_10

Installez Poetry (si vous ne l'avez pas déjà installé) :
curl -sSL https://install.python-poetry.org | python3 -

Installez les dépendances du projet en utilisant Poetry :
poetry install

## Utilisation:
Activez l'environnement virtuel créé par Poetry :
poetry shell

Exécutez le programme en utilisant Poetry :
python manage.py runserver