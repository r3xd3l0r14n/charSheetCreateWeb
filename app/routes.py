from flask import render_template, send_file, redirect, url_for, jsonify, request, session
from app import app
from app.forms import *
from app.character import Character
import json, os

app.secret_key = "asd93j2jf04kv93vn1nvjd2et"

char = Character()
cwd = os.getcwd()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Starfinder')


@app.route('/charN', methods=['GET', 'POST'])
def charN():
    form = charNForm()
    if form.validate_on_submit():
        session['char'] = form.charN.data
        session['race'] = form.race.data
        session['gender'] = form.gender.data
        return redirect(url_for('charTheme'))
    return render_template('charStart.html', title="Create new Char", form=form)


@app.route('/charTheme', methods=['GET', 'POST'])
def charTheme():
    form = charThemeForm()
    if form.validate_on_submit():
        print(session)
        session['theme'] = form.theme.data
        return redirect(url_for('charClass'))
    return render_template('charTheme.html', title="Select Theme and Level", form=form)


@app.route('/charClass', methods=['GET', 'POST'])
def charClass():
    if request.method == 'POST':
        n = session['class']
        s = 'charSel' + n
        return redirect(url_for(s))
    return render_template('charClass.html', title="Pick A Class")


# Character Ability Description and Selection Screens
# TODO - return to this to make it more concise 11/27/2018 CRD
@app.route('/charSelectionEnvoy', methods=['GET', 'POST'])
def charSelEnvoy():
    if request.method == 'POST':
        v = request.form['sel1']
        session['improvs'] = v
        return redirect(url_for('rollAttrib'))
    return render_template('classSel/charSelEnvoy.html', title="Envoy")


@app.route('/charSelectionMechanic')
def charSelMechanic():
    return render_template('classSel/charSelMechanic.html', title="Mechanic")


@app.route('/charSelectionSolarian', methods=['GET', 'POST'])
def charSelSolarian():
    if request.method == 'POST':
        v = request.form['sel1']
        session['slrMan'] = v
        return redirect(url_for('rollAttrib'))
    return render_template('classSel/charSelSolarian.html', title="Solarian")


@app.route('/charSelectionMystic')
def charSelMystic():
    return render_template('classSel/charSelMystic.html', title="Mystic")


@app.route('/charSelectionTechnomancer')
def charSelTechnomancer():
    return render_template('classSel/charSelTechnomancer.html', title="Technomancer")


@app.route('/charSelectionSoldier')
def charSelSoldier():
    return render_template('classSel/charSelSoldier.html', title="Soldier")


@app.route('/charSelectionOperative', methods=['GET', 'POST'])
def charSelOperative():
    if request.method == 'POST':
        v = request.form['sel1']
        session['ospecs'] = v
        return redirect(url_for('rollAttrib'))
    return render_template('classSel/charSelOperative.html', title="Operative")


# Rolling Attributes screen
@app.route('/rollAttrib', methods=['GET', 'POST'])
def rollAttrib():
    if request.method == 'POST':
        return redirect(url_for("selSkills"))
    return render_template('rollAttrib.html', title='Roll Attributes')


@app.route('/selSkills', methods=['GET', 'POST'])
def selSkills():
    if request.method == 'POST':
        #char.createPDF(session)
        return redirect(url_for("feats"))  # TODO - Change this back later
        #return redirect(url_for('show_static_pdf'))
    return render_template('selSkills.html', title='Select Skills')


@app.route('/feats', methods=['GET', 'POST'])
def feats():
    if request.method == 'POST':
        char.createPDF(session)
        return redirect(url_for('show_static_pdf'))
    return render_template('feats.html', title='Feats')


# Final Screen to show the pdf Files
@app.route('/show/static-pdf')
def show_static_pdf():
    return send_file(cwd+'/app/destination.pdf', mimetype='application/pdf', attachment_filename='file.pdf')


###################################
### HELPER ROUTES
###################################
@app.route('/get_theme/<theme>')
def get_theme(theme):
    with open(cwd + '/app/json/theme.json', 'rb') as file:
        themes = json.load(file)
    if theme in themes:
        print(jsonify(themes[theme]))
        return jsonify(themes[theme])
    else:
        return "Could not find requested item! Please try again!"


@app.route('/get_class/<charCls>')
def get_class(charCls):
    charClsJson = cwd + '/app/json/classes/' + charCls.lower() + '.json'
    session['class'] = charCls
    with open(charClsJson, 'rb') as file:
        charClsFile = json.load(file)
    return jsonify(charClsFile)



@app.route('/get_attrib')
def getAttrib():
    with open(cwd + '/app/json/attrib.json', 'rb') as f:
        attribJSON = json.load(f)
    attribJSON['roll'] = char.rollAtr()
    return jsonify(attribJSON)


@app.route('/getSkills')
def getSkills():
    with open(cwd + '/app/json/skills.json', 'rb') as f:
        skillJSON = json.load(f)
    skillJSON['class'] = session['class'].lower()
    with open(cwd + '/app/json/classes/' + skillJSON['class'].lower() + '.json', 'rb') as f:
        cls = json.load(f)
    ABM = char.abMods[session['attr'][cls['sRanksABM']]]
    ranks = cls['sRanks']
    skillJSON['ranks'] = int(ABM) + int(ranks)
    skillJSON['abMod'] = char.atribMod
    return jsonify(skillJSON)


@app.route('/setAttrib', methods=['GET', 'POST'])
def setAttrib():
    session['attr'] = request.json
    char.checkAttribs(session['attr'])  # This sets the skills at the same time
    return "Got the message"


@app.route('/setSkills', methods=['GET', 'POST'])
def setSkill():
    data = request.json
    session['skills'] = data
    session['sRanks'] = char.setSkills(data, session['class'])
    return "Got the message"

@app.route('/setFeats', methods=['GET', 'POST'])
def setFeats():
    data = request.json
    session['feats'] = char.setFeats(data, session['class'])

@app.route('/killSession')
def killSession():
    session.pop('username', None)
    return redirect(url_for('index'))
