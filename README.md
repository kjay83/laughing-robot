# laughing-robot
python projects to refresh memory, using for instance django
-- projet Employe cf video youtube https://www.youtube.com/watch?v=qRc0aeohMIg
---pour lancer le projet, en ligne de commande se mettre a la racine du projet puis
---l'environnement s'appelle faiz1 donc
----activer l'environnement avec "faiz1\Scripts\activate.bat"
----bien s'assurer que le nom de l'envirronement s'affiche dans le prompt
----lancer le serveur avec "python ./manage.py runserver"
NB: admin user=admin mdp=admin
COMMANDES UTILES :
-- "py .\manage.py loaddata app_name/fixtures/nom_fichier.json" pour charger la bdd avec des données
-- "py manage.py flush" pour reinitialiser TOUTE la BDD
-- "py manage.py dumpdata app_name.Class_name app_name.Class_name2 --indent 4 > app_name/fixtures/nom_fichier.json" pour dumper des donnees de plusieurs tables de l'app