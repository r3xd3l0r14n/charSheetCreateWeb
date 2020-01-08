from PyPDF2 import PdfFileWriter, PdfFileReader
import io, random, os, json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


cwd = os.getcwd()

with open(cwd+'/app/json/skills.json', 'rb') as f:
    mSkills = json.load(f)
with open(cwd+'/app/json/feats.json', 'rb') as f:
    mFeats = json.load(f)
class Character():
    attrRoll = []
    attribs = {}
    atribMod = {}
    abMods = {"1": "-5", "2": "-4", "3": "-4", "4": "-3", "5": "-3", "6": "-2", "7": "-2", "8": "-1", "9": "-1",
              "10": "0", "11": "0", "12": "1", "13": "1", "14": "2", "15": "2", "16": "3", "17": "3", "18": "4",
              "19": "4", "20": "5"}

    # def __init__(self, name=None, race=None, gender=None, theme=None, cls=None, improvs=None, attribs=None, atribMod=None):
    #     self.race = race
    #     self.name = name
    #     self.gender = gender
    #     self.theme = theme
    #     self.cls = cls
    #     self.improvs = improvs
    #     self.attribs = attribs
    #     self.atribMod = atribMod

    def rollAtr(self):
        x = 0
        attrDict = []
        while x < 6:
            i = []
            for f in range(0, 4):
                i.append(random.randint(1, 6))
                f += 1
            i.remove(min(i))
            attrDict.append(sum(i))
            x += 1
        self.attrRoll = attrDict
        return attrDict

    def checkAttribs(self, data):
        met = data['method']
        if met == 'pB':
            for k, v in data.items():
                print(v)  # TODO - Actually finish this section CRD 07Dec2018
        elif met == 'qpF':
            for k, v in data.items():
                if v == 'qpF':
                    print("Method is QPF")
                elif v == "18" or "14" or "11" or "10":
                    self.attribs[k] = v
                    self.atribMod[k] = self.abMods[v]

        elif met == 'qpS':
            for k, v in data.items():
                if v == 'qpf':
                    print('method is QPS')
                elif v == 16 or 11 or 10:
                    self.attribs[k] = v
                    self.atribMod[k] = self.abMods[v]

        elif met == 'qpV':
            for k, v in data.items():
                if v == 'qpF':
                    print("Method is QPV")
                elif v == 14 or 11 or 10:
                    self.attribs[k] = v
                    self.atribMod[k] = self.abMods[v]

        elif met == 'rS':
            for k, v in data.items():
                if v == "rS":
                    pass
                elif int(v) in self.attrRoll:
                    self.attribs[k] = v
                    self.atribMod[k] = self.abMods[v]

    def setSkills(self, data, cls):
        self.skills = data
        with open(cwd+'/app/json/classes/'+cls.lower()+'.json', 'rb') as f:
            clsFile = json.load(f)
        self.sRanks = int(clsFile['sRanks'])+int(self.atribMod[clsFile['sRanksABM']])
        return self.sRanks
        #TODO - Finish this section for final CRD 12/24/2018

    def createPDF(self, ses):
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(155, 753, ses['char'])  # Draw the name on the top
        can.drawString(215, 731, ses['race'])  # Draw our character race on the sheet
        can.drawString(165, 710, ses['gender'])  # Draw gender
        can.drawString(20, 730,  ses['class'])  # Draw Class
        can.drawString(315, 730, ses['theme'])  # Theme
        can.drawString(256.5, 483, str(ses['sRanks']))  # Draw skill levels
        # Draw ability scores
        can.drawString(95, 620, ses['attr']['str'])  # Str
        can.drawString(142, 620, self.abMods[ses['attr']['str']])  # Str Mod
        can.drawString(95, 599, ses['attr']['dex'])  # DEX
        can.drawString(142, 599, self.abMods[ses['attr']['dex']])  # DEX Mod
        can.drawString(95, 578, ses['attr']['con'])  # CON
        can.drawString(142, 578, self.abMods[ses['attr']['con']])  # CON Mod
        can.drawString(95, 556, ses['attr']['int'])  # INT
        can.drawString(142, 556, self.abMods[ses['attr']['int']])  # INT Mod
        can.drawString(95, 535, ses['attr']['wis'])  # WIS
        can.drawString(142, 535, self.abMods[ses['attr']['wis']])  # WIS Mod
        can.drawString(95, 514, ses['attr']['cha'])  # CHA
        can.drawString(142, 514, self.abMods[ses['attr']['cha']])  # CHA Mod
        # This draws all most if not all of our class skill related data on the sheet
        for s in mSkills:
            if ses['class'].lower() in mSkills[s]['class']:
                x = float(mSkills[s]["pos"]["x"])
                y = float(mSkills[s]["pos"]["y"])
                can.drawImage('10003.png', x, y, 10, 8,
                              mask=[255, 255, 255, 255, 255, 255])
            if mSkills[s]['name'] in ses['skills']:
                nm = mSkills[s]
                # Total First
                can.drawString(nm['pos']['xTot'], nm['pos']['yTot'], str(ses['skills'][nm['name']]['tot']))
                # Ranks
                can.drawString(nm['pos']['xRnk'], nm['pos']['yRnk'], ses['skills'][nm['name']]['rnk'])
                # Bonus
                can.drawString(nm['pos']['xBon'], nm['pos']['yBon'], ses['skills'][nm['name']]['bon'])
                # Ability Mod
                can.drawString(nm['pos']['xAbm'], nm['pos']['yAbm'], ses['skills'][nm['name']]['abm'])
        for s in mFeats:
            print(s)
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open(cwd+"/app/original.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page2 = existing_pdf.getPage(1)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        output.addPage(page2)
        # finally, write "output" to a real file
        # TODO - This needs to be fixed such that it won't create a file with the same name CRD 12/27/18
        outputStream = open(cwd+"/app/destination.pdf", "wb")
        output.write(outputStream)
        outputStream.close()

### toJson Method
    def toJson(self):
        finJ = {"charN":self.name}
        return finJ


