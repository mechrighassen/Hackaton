Dependances :
Flask
mysql
sklearn
Keras
pandas


Pour que le programme python se connecte a la base mysql :
Creer un fichier ".database-credential.json" qui contient les informations de connexion a la base mysql locale
c'est a dire : host,user,password,database

Faire des requetes avec les parametres :
Requetes                    : Parametres
1.POST: MODEL/ADD           : Model Name/Parameters
2.GET: MODEL/{id}
3.DEL: MODEL/{id}
4.POST: MODEL/{id}          : Model Name/Arguments
5.POST: MODEL/{id}/TRAIN    : Path of Train File
6.GET: MODEL/{id}/PREDICT   : Path of Test File
7.GET: MODEL/

datasets dans ./lib/data
modeles enregistres dans ./models


