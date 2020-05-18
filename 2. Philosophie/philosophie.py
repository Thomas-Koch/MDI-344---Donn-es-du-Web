#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage


app = Flask(__name__)

app.secret_key = "96NZnk)v6h?F3P["

global table_content
    

global val


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Bonjour, monde !")

# Si vous définissez de nouvelles routes, faites-le ici

#-------------------- NEW-GAME --------------------
@app.route('/new-game', methods=['POST'])
def new_game():
    session["score"]=0
    
    if 'start_auto' in request.form:
        session['article'] = request.form['nom_page']
        return redirect('/autogame')
    else:
        session['article'] = request.form['nom_page']
        return redirect('/game')
    
    
#-------------------- GAME --------------------
@app.route('/game', methods=['GET'])
def game() :
    session['title'], session['hrefs'] = getPage(session['article'])
    
    if session['title'] == 'Philosophie' :
        with open("score.txt", "a") as d:
            d.write(str(str(session['article']) + ',' + str(session['score']) + ',' + 'False')+'\n')
            d.close()
            
        flash("Bravo, vous avez gagné ! Votre score est de : " + str(session['score']), "Won")
        return redirect('/')
        
    if session['title'] == None :
        flash("Dommage, c'est perdu... La page demandée n'existe pas.", "Lost")
        return redirect('/')

    if session['hrefs'] == [] :
        flash("Dommage c'est perdu... La page demandée n'a pas de liens.", "Lost")
        return redirect('/')
        
    else :
        session['score'] += 1
        return render_template('game.html', title=session['title'], hrefs=session['hrefs'] )



#-------------------- MOVE --------------------
@app.route('/move', methods=['POST'])
def move() :
    if request.form['destination'] in session['hrefs'] :
        session['article'] = request.form['destination']
        return redirect('/game')
    else :
        flash("Vous jouez sur plusieurs onglets.", "Lost")
        return redirect('/')

   


if __name__ == '__main__':
    app.run(debug=True)

