from random import choice
from pickle import dump,load
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

class Graphe:
    """
    Classe permetant de stocker et de gérer un graphe complet.

    Attributes
    ----------
    adj : dict
        Le dictionnaire d'adjacence du graphe.
    """
    def __init__(self)->None:
        """
        Initialise une instance vide de Graphe.
        """
        self.adj = {}
    def ajouter_noeud(self,nouv_noeud:str)->None:
        """
        Ajoute un noeud dans le graphe.

        Parameters
        ----------
        nouv_noeud : str
            Le noeud à ajouter.
        """
        assert type(nouv_noeud) == str, f"Erreur de format, le noeud doit être de type str, et non pas de type {type(nouv_noeud)}."
        if nouv_noeud not in self.adj:
            self.adj[nouv_noeud] = []
    def ajouter_arête(self,noeud1:str,noeud2:str)->None:
        """
        Ajoute au graphe l'arête partant du noeud1 et allant jusqu'au noeud2.

        Parameters
        ----------
        noeud1 : str
            Le noeud qui possède noeud2 en voisin sortant.
        noeud2 : str
            Le noeud qui possède noeud1 en voisin entrant.
        """
        assert type(noeud1) == str, f"Erreur de format, le premier noeud doit être de type str, et non pas de type {type(noeud1)}."
        assert type(noeud2) == str, f"Erreur de format, le deuxième noeud doit être de type str, et non pas de type {type(noeud2)}."
        self.ajouter_noeud(noeud1)
        self.ajouter_noeud(noeud2)
        self.adj[noeud1].append(noeud2)
    def voisins(self,noeud:str)->list:
        """
        Permet de récupérer la liste des voisins d'un noeud au sein du graphe.

        Parameters
        ----------
        noeud : str
            Le noeud dont on souhaite récupérer ses voisins.
        
        Returns
        -------
        list :
            La liste des noeuds voisins sortant de noeud.
        """
        assert type(noeud) == str, f"Erreur de format, le noeud doit être de type str, et non pas de type {type(noeud)}."
        self.ajouter_noeud(noeud)
        return self.adj[noeud]
    def visualiser(self)->None:
        """
        Permet de visualiser le graphe grâce à networkx et matplotlib.
        """
        G = nx.DiGraph()  # Créer un graphe dirigé
        for mot in self.adj:
            for derive in self.adj[mot]:
                G.add_edge(mot, derive)  # Ajouter une arête pour chaque dérivation
        nx.draw(G, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_color='black')
        plt.title("Visualisation du Graphe")
        plt.show()  # Afficher le graphe
class GrapheMarkov(Graphe):
    """
    Sous-classe de la classe Graphe permetant de stocker et de gérer un graphe complet appliqué au problème de la chaîne de Markov.

    Additional attributes
    ---------------------
    nom : str
        Le nom du graphe et, dans le cas d'une exportation avec Pickle, le nom du fichier pickle.
    trajets : list
        La liste des trajets possibles (utile lors de l'application d'une mémoire à la chaîne de Markov).
    """
    def __init__(self,nom:str="étude")->None:
        """
        Initialise une instance de GrapheMarkov.

        Parameters
        ----------
        nom : str, optional
            Le nom du graphe et, dans le cas d'une exportation avec Pickle, le nom du fichier pickle au format str (par défaut "étude").
        """
        super().__init__()
        self.trajets = []
        self.nom = nom
    def ajouter_trajet(self,liste_noeuds:list[str])->None:
        """
        Ajouter au Graphe de Markov un trajet (c'est-à-dire une liste de mot qui peuvent se suivre dans une phrase).

        Parameters
        ----------
        liste_noeuds : list[str]
            Une liste d'éléments de type str qui peuvent se suivre lors de la méthode héritage. Attention, tous les trajets doivent être de la même taille.
        """
        assert len(self.trajets) == 0 or len(liste_noeuds) == len(self.trajets[0]), "Tous les trajets ne sont pas de la même taille."
        self.trajets.append(tuple(liste_noeuds))
    def héritage(self,liste_noeuds:list[str])->str:
        """
        Permet de connaître quel Noeud suit une liste de noeud selon un tirage aléatoire.

        Parameters
        ----------
        liste_noeuds : list[Noeud]
            Une liste d'objet de la classe Noeud qui peuvent se suivre lors de la méthode héritage.

        Returns
        -------
        Noeud :
            L'objet de type Noeud, héritié de la liste de noeuds fournie.
        """
        assert type(liste_noeuds) == list and 0<len(liste_noeuds) and len(liste_noeuds)<=len(self.trajets[0]) and all(type(noeud) == str for noeud in liste_noeuds), "La liste fournie ne répond pas aux critères."
        trajets_possibles = []
        for trajet in self.trajets:
            if trajet[len(self.trajets[0])-len(liste_noeuds)-1:-1] == tuple(liste_noeuds): # On vérifie si liste_noeuds correspond au paterne de fin du trajet (sauf le dernier noeud de ce trajet).
                trajets_possibles.append(trajet[-1]) # On ajoute le dernier élément.
        if trajets_possibles != []:
            return choice(trajets_possibles)
        return choice(list(self.adj.keys())) # Si aucun élément n'as été trouvé, on retourne un noeud aléatoire.
    def __str_from_liste(self,liste_parents:list[str],taille:int=15):
        """
        Permet d'obtenir une chaine de caractère d'un certain nombre de mots à partir d'une liste de mots de début.
        Attention, aucune vérification n'est effectuée sur la liste de mots fournie par l'utilisateur, il faut donc être sûr de l'intégrité des donnés fournies.
        
        Parameters
        ----------
        mots_de_début : list[str]
            La liste de mots à partir de laquelle on souhaite créer notre texte. 
            Attention, aucune vérification n'est effectuée sur cette liste, il faut donc être sûr de l'intégrité des donnés fournies.
        taille : int, optional
            Le nombre de mots demandés dans le texte généré, par défaut sur 15.
        
        Returns
        -------
        str :
            Une chaine de caractère d'un certain nombre de mots à partir d'une liste de mots.
        """
        retournement = ""
        for parent in liste_parents:
            retournement += str(parent) + " "
        for i in range(taille-len(liste_parents)):
            liste_parents.append(self.héritage(liste_parents))
            liste_parents.pop(0)
            retournement += liste_parents[-1] + " "
        return retournement
    def ajouter_paragraphe(self,p:str,taille_trajets:int=6)->None:
        """
        Permet d'ajouter tous les mots d'un paragraphe au graphe.

        Parameters
        ----------
        p : str
            Le paragraphe au format str
        taille_trajets : int, optional
            La taille des trajets que l'on souhaite créer, la valeur par défaut est 6. Attention, si des trajets sont déjà présents, cette valeur sera ignorée.
        """
        if len(self.trajets) != 0:
            taille_trajets = len(self.trajets[0]) # Pour éviter les erreurs, met taille_trajets à la taille des autres trajets si d'autres trajets existent.
        liste_mots = []
        mot = ""
        stop_liste = [".","?","!",";",":",",",'"',"(",")","«","»","_"," ","'","-","\n"] # La liste des caractères séparateurs de mots dans une phrase.
        for caractère in p:
            if caractère in stop_liste:
                if mot != "":
                    liste_mots.append(mot.lower()) # Ajoute chaque mot en minuscule à la liste des mots présents.
                    mot = ""
            else:
                mot += caractère
        if mot != "":
            liste_mots.append(mot.lower()) # Ajoute le dernier mot.
        assert 1 < taille_trajets < len(liste_mots), "Le nombre de mots dans le paragraphe doit être plus grand que taille_trajets."
        for i in range(1,taille_trajets): # Boucle permetant d'ajouter les premeiers mots dans le graphe et leur trajets pour les cas où on utilise un niveau d'intelligence moins fort que le maximum.
            self.ajouter_arête(liste_mots[i-1],liste_mots[i])
            liste_trajet = [None for j in range(taille_trajets-i)] # On ajoute des None pour les mots qui n'éxistent pas de façon à éviter tout bug au niveau de la taille des trajets. Ils ne seront de toute façon jamais parcourus.
            liste_trajet.extend([liste_mots[i+j] for j in range(-i+1,1)])
            self.ajouter_trajet(liste_trajet)
        for i in tqdm(range(taille_trajets,len(liste_mots)-1)): # On répète pour tous les mots non-créés.
            self.ajouter_arête(liste_mots[i-1],liste_mots[i])
            self.ajouter_trajet([liste_mots[i+j] for j in range(-taille_trajets,0)]) # Permet de gérer la longueur n grâce aux indice.
        self.ajouter_arête(liste_mots[-2],liste_mots[-1])
        self.ajouter_trajet([liste_mots[len(liste_mots)+j] for j in range(-taille_trajets,0)]) # Ajoute le dernier trajet.
    def str(self,taille:int=100,mot_de_début:str=None,intel:int=3):
        """
        Permet d'obtenir une chaine de caractère d'un certain nombre de mots à partir d'un mot de début et avec un certain niveau d'intelligence.

        Parameters
        ----------
        taille : int optional
            Le nombre de mots demandés dans le texte généré, par défaut sur 100.
        mot_de_début : str, optional
            Si possible, le premier mot de la chaîne générée, par défaut sur None (et donc un mot aléaatoire).
        intel : int, optional
            La mémoire du programme (1 équivaut au programme de Marov original), par défaut sur 3 (qui n'est pas forcément une valeure valide).
        
        Returns
        -------
        str :
            Une chaine de caractère d'un certain nombre de mots à partir d'un mot de début et avec un certain niveau d'intelligence.
        """
        assert 0 < intel < len(self.trajets[0]), "Le niveau d'intelligence demandé n'éxiste pas."
        assert taille > intel, "On ne peut pas générer moins de caractères que le niveau d'intelligence."
        if mot_de_début is not None and mot_de_début in self.adj: # Met le premier élément dans liste_parents.
            liste_parents = [mot_de_début]
        else:
            liste_parents = [choice(list(self.adj.keys()))]
        for g in range(intel-1):
            liste_parents.append(self.héritage(liste_parents)) # On ajoute tous les premiers noeuds selon le niveau d'intelligence.
        return self.__str_from_liste([str(noeud) for noeud in liste_parents],taille)
    def __str__(self)->str:
        """
        Retourne le résultat de self.str() avec ses valeurs par défaut.

        Returns
        -------
        str :
            Le résultat de self.str() avec ses valeurs par défaut.
        """
        return self.str()
    def export(self)->None:
        """
        Exporte le graphe dans un fichier .pickle positionné dans le dossier pickle. Attention, ce dossier doit éxister.
        """
        if not os.path.exists("pickle"):
            os.mkdir("pickle")
        dump(self,open("./pickle/" + self.nom + ".pickle","wb"))
def créer_multi_graphe(nom:str,fichiers_txt:list)->None:
    """
    Permet de créer et d'exporter un graphe basé sur l'algorithme de Markov avec plusieurs fichiers txt.
    
    Parameters
    ----------
    nom : str
        Le nom du fichier pickle à créer.
    fichiers_txt : list
        La liste des noms des fichiers au format txt avec leur extension. Attention, ces fichiers doivent se trouver dans un dossier "textes". 
    """
    mon_etude = GrapheMarkov(nom)
    for fichier in fichiers_txt:
        with open("textes/"+fichier,"r",encoding="utf-8") as fichier:
            mon_etude.ajouter_paragraphe(fichier.read(),6)
    mon_etude.export()

def créer_graphe(fichier_txt:str)->None:
    """
    Permet de créer et d'exporter un graphe basé sur l'algorithme de Markov avec un seul fichier txt.
    
    Parameters
    ----------
    fichier_txt : str
        Le nom du fichier txt avec son extension. Attention, ce fichier doit se trouver dans un dossier "textes".
    """
    assert fichier_txt[-4:] == ".txt", "Le fichier doit être au format .txt"
    assert os.path.exists("textes/"+fichier_txt), "Le fichier texte n'existe pas dans le dossier textes."
    mon_etude = GrapheMarkov(fichier_txt[:-4])
    with open("textes/"+fichier_txt,"r",encoding="utf-8") as fichier:
        mon_etude.ajouter_paragraphe(fichier.read(),6)
    mon_etude.export()
def ouvrir_graphe(nom:str)->GrapheMarkov:
    """
    Permet d'ouvrir un graphe à partir de son nom au format pickle.
    
    Parameters
    ----------
    nom : str
        Le nom du fichier pickle avec son extension. Attention,ce fichier doit se trouver dans un dossier "pickle"
    
    Returns
    -------
    GrapheMarkov :
        Le graphe qui était contenu dans le fichier pickle.
    """
    return load(open(nom,"rb"))

if __name__ == "__main__":
    if input("Souhaitez-vous configurer le projet pour un nouveau texte (Attention, cela peut durer plusieurs minutes) ? (oui/non) ") == "oui":
        if os.path.exists("textes") == False:
            os.mkdir("textes")
        input("Lorsque vous aurez mis le texte dans le dossier textes, appuyez sur Entrée pour continuer. ")
        créer_graphe(input("Quel est le nom du fichier texte ? (avec l'extension) "))