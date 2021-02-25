# Extension ASA Périmètre

Une extension qui permet d'effectuer une jointure entre
les données parcellaires et un fichier métier.

Pour utiliser cette extension il suffit de cliquer sur le bouton
"ASA jointure Perimètre" présent dans l'image ci-dessous qui
lancera l'algorithme de jointure.

![panneauasa](perimetre_asa/resources/images/panneauasa.png)


Voici l'interface de l’algorithme de jointure, il dispose de
trois paramètres : le premier concerne la couche des parcelles,
le deuxième la couche rôle et le dernier le dossier où l'on
veut sauvegarder la couche périmètre.

![Algo](perimetre_asa/resources/images/algoasa.png)


Pour les deux premiers paramètres soit vous avez les couches dans
un projet QGIS et alors vous pourrez les sélectionner via liste
déroulante. Soit vous cliquez sur le bouton avec trois points dessous
et une boîte de sélection de fichiers s'ouvre comme l'image ci-dessous
ou vous irez chercher vos fichiers de données comme le
fichier concernant la couche rôle.

![panneauasa](perimetre_asa/resources/images/getFile.png)


Pour le dernier paramètre il vous faut cliquer sur le bouton
avec les trois points. Une liste de choix s'offre vous, il vous
faut cliquer sur "Enregistrer vers un fichier..." qui vous ouvrira
une boîte comme l'image ci-dessous pour sélectionner le dossier
de sortie et le nom que vous donnerez à la couche ex : périmètre.shp

![panneauasa](perimetre_asa/resources/images/getFolder.png)


Pour finir il vous restera à cliquer sur le bouton "Exécuter" en bas
à droite de l'interface de l'algorithme présent sur la deuxième image.
