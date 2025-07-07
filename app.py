from flask import Flask,render_template,request
from os import listdir
from projet import *

app = Flask(__name__)
@app.route("/",methods=['GET', 'POST'])
def recherche():
    """
    Fonction basé sur le tutoriel suivant : https://info-mounier.fr/terminale_nsi/base_de_donnees/tp-flask-sqlite (founi par mmonsieur MONNIER M)
    """
    if request.method == "POST":
        donnees = request.form
        if donnees.get("form_id") == "f1":
            mot = donnees.get("mot")
            source = donnees.get("source")
            taille = donnees.get("nb_mots")
            inteligence = donnees.get("intel")
            génération = ouvrir_graphe("./pickle/"+source).str(int(taille),mot.lower(),int(donnees.get("intel")))
        elif donnees.get("form_id") == "f2":
            gen_précédente = donnees.get("content")
            
            source = donnees.get("livre")
            inteligence = donnees.get("inteligence")
            mots = gen_précédente.split(" ")[-int(inteligence)-1:-1]
            taille = 0
            for mot in mots:
                taille += len(mot) + 1
            génération = gen_précédente[:-taille]+" "+ouvrir_graphe("./pickle/"+source)._GrapheMarkov__str_from_liste(mots)
        else:
            inteligence = None
            source = None
            génération = None
    else:
        inteligence = None
        source = None
        génération = None

    return render_template("recherche.html", génération=génération,li=listdir("./pickle"),livre=source,inteligence=inteligence)

if __name__ == "__main__":
    app.run(debug=True)