from flask import render_template, send_file, redirect, url_for, jsonify, request
from app import app
from app.forms import *
from app.character import Character
import json, os

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
        char.setNameRace(form.charN.data, form.race.data, form.gender.data)
        # char.createPDF()
        # return redirect(url_for('show_static_pdf'))
        return redirect(url_for('charTheme'))
    return render_template('charStart.html', title="Create new Char", form=form)


@app.route('/charTheme', methods=['GET', 'POST'])
def charTheme():
    form = charThemeForm()
    if form.validate_on_submit():
        char.setTheme(form.theme.data)
        return redirect(url_for('charClass'))
    return render_template('charTheme.html', title="Select Theme and Level", form=form)


@app.route('/charClass', methods=['GET', 'POST'])
def charClass():
    # form = charClassForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('sel_char'))
    if request.method == 'POST':
        n = char.cls
        s = 'charSel'+n
        return redirect(url_for(s))
    return render_template('charClass.html', title="Pick A Class")

#Character Ability Description and Selection Screens
# TODO - return to this to make it more concise 11/27/2018 CRD
@app.route('/charSelectionEnvoy', methods=['GET', 'POST'])
def charSelEnvoy():
    if request.method == 'POST':
        v = request.form['sel1']
        char.setImprovs(v)
        return redirect(url_for('rollAttrib'))
    return render_template('classSel/charSelEnvoy.html', title="Envoy")

@app.route('/charSelectionMechanic')
def charSelMechanic():
    return render_template('classSel/charSelMechanic.html', title="Mechanic")

@app.route('/charSelectionSolarian')
def charSelSolarian():
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

@app.route('/charSelectionOperative')
def charSelOperative():
    return render_template('classSel/charSelOperative.html', title="Operative")

#Rolling Attributes screen
@app.route('/rollAttrib', methods=['GET','POST'])
def rollAttrib():
    if request.method == 'POST':
        return redirect(url_for("selSkills"))
    return render_template('rollAttrib.html', title='Roll Attributes')

@app.route('/selSkills', methods=['GET', 'POST'])
def selSkills():
    if request.method == 'POST':
        char.createPDF()
        return redirect(url_for("feats")) #TODO - Change this back later
    return render_template('selSkills.html', title='Select Skills')

@app.route('/feats', methods=['GET', 'POST'])
def feats():
    return render_template('feats.html', title='Feats')


#Final Screen to show the pdf Files
@app.route('/show/static-pdf')
def show_static_pdf():
    return send_file('../destination.pdf', mimetype='application/pdf', attachment_filename='file.pdf')


###################################
### HELPER ROUTES
###################################
@app.route('/get_theme/<theme>')
def get_theme(theme):
    with open(cwd+'/app/json/theme.json', 'rb') as file:
        themes = json.load(file)
    if theme in themes:
        print(jsonify(themes[theme]))
        return jsonify(themes[theme])
    else:
        return "Could not find requested item! Please try again!"


@app.route('/get_class/<charCls>')
def get_class(charCls):
    charClsJson = cwd + '/app/json/classes/' + charCls.lower() + '.json'
    char.setClass(charCls)
    with open(charClsJson, 'rb') as file:
        charClsFile = json.load(file)
    if charCls == "Envoy":
        return jsonify(charClsFile)
    elif charClsFile[charCls]:
        return jsonify(charClsFile)

@app.route('/get_attrib')
def getAttrib():
    with open(cwd+'/app/json/attrib.json', 'rb') as f:
        attribJSON = json.load(f)
    attribJSON['roll'] = char.rollAtr()
    return jsonify(attribJSON)

@app.route('/getSkills')
def getSkills():
    with open(cwd +'/app/json/skills.json', 'rb') as f:
        skillJSON = json.load(f)
    skillJSON['class'] = char.cls.lower()
    with open(cwd+'/app/json/classes/'+skillJSON['class'].lower()+'.json', 'rb') as f:
        cls = json.load(f)
    ABM = char.abMods[char.attribs[cls['sRanksABM']]]
    ranks = cls['sRanks']
    skillJSON['ranks'] = int(ABM)+int(ranks)
    skillJSON['abMod'] = char.atribMod
    return jsonify(skillJSON)

@app.route('/setAttrib', methods=['GET', 'POST'])
def setAttrib():
    data = request.json
    char.checkAttribs(data) #This sets the skills at the same time
    return "Got the message"

@app.route('/setSkills', methods=['GET', 'POST'])
def setSkill():
    data = request.json
    char.setSkills(data)
    return "Got the message"

