#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Bonjour, monde !")

# Si vous définissez de nouvelles routes, faites-le ici

@app.route('/newgame', methods=['POST'])
def new_game():
    session["score"]=0
    
    if 'start_auto' in request.form:
        session['article'] = request.form['nom_page']
        return redirect('/autogame')
    else:
        session['article'] = request.form['nom_page']
        return redirect('/game')
    
# arrêt question 3.4 pour ajouter route game

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

