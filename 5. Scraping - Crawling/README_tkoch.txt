Rq : Le présent fichier est écrit au format markdown pour un affichage plus stylisé. Il est cependant lisible en format txt brut.


# Etape 7

***Thomas KOCH***


## Rôle général d'une méthode comme `linksfilter` dans une application de crawling :

Le rôle général d'une méthode comme `linksfilter` dans une application de crawling est de permettre **d'éliminer les redirections inutiles pour notre cas d'application**. Citons par exemple les liens de partage Twitter ou vers des styles `.css`.

Nous pouvons ajouter à cela le fait qu'une telle méthode permette de **réduire le nombre de liens considérés** tout comme **d'éviter l'exploration multiple d'un même lien**, ce qui fait perdre du temps de calcul inutilement.



## Rôle général d'une méthode comme `contentfilter` dans une application de crawling

Le rôle général d'une méthode comme `contentfilter` dans une application de crawling est avant tout de **permettre la sélection des liens contenant de l'information utile à notre exploration du web**. Cette méthode est donc liées aux informations que l'on souhaite retrouver.


## Limites du code proposé à l'étape 6

J'identifie glogalement **4 limites au code proposé** :

- Il ne peut pas être directement utilisé pour une langue autre que le français.

- Il ne peut pas s'appliquer à un autre site internet.

- Une page peut contenir un mot clé comme *Inventors* mais ne pas contenir l'information qui nous intéresse (ici le ou les noms des inventeurs).

- Il faut connaître à l'avance les mots clés à rechercher dans le site pour trouver l'information que l'on souhaite obtenir.

