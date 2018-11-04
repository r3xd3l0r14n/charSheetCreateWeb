from flask import render_template, send_file, redirect, url_for, jsonify
from app import app
from app.forms import charNForm, charClassForm
from app.character import Character
import json

char = Character()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Starfinder')


@app.route('/charN', methods=['GET', 'POST'])
def charN():
    form = charNForm()
    if form.validate_on_submit():
        char.setNameRace(form.charN.data, form.race.data, form.gender.data)
        # char.createPDF()
        # return redirect(url_for('show_static_pdf'))
        return redirect(url_for('charClass'))
    return render_template('charN.html', title="Create new Char", form=form)


@app.route('/charClass', methods=['GET', 'POST'])
def charClass():
    form = charClassForm()
    if form.validate_on_submit():
        char.setClassTheme(form.charCls.data, form.theme.data)
        char.createPDF()
        return redirect(url_for('show_static_pdf'))
    return render_template('charClass.html', title="Stage 2 of Character Creation", form=form)


@app.route('/show/static-pdf')
def show_static_pdf():
    return send_file('../destination.pdf', mimetype='application/pdf', attachment_filename='file.pdf')


@app.route('/get_theme/<theme>')
def get_theme(theme):
    with open('json/theme.json', 'rb') as file:
        themes = json.load(file)
    if theme in themes:
        print(jsonify(themes[theme]))
        return jsonify(themes[theme])
    else:
        return "Could not find requested item! Please try again!"


@app.route('/get_class/<charCls>')
def get_class(charCls):
    with open('json/classes.json', 'rb') as file:
        classes = json.load(file)
    if charCls in classes:
        return jsonify(classes[charCls])
    else:
        return "Could not find requested item! Please try again!"
