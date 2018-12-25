from PyPDF2 import PdfFileWriter, PdfFileReader
import io, random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class Character:
    attrRoll = []
    attribs = {}
    atribMod = {}
    abMods = {"1": "-5", "2": "-4", "3": "-4", "4": "-3", "5": "-3", "6": "-2", "7": "-2", "8": "-1", "9": "-1",
              "10": "0", "11": "0", "12": "1", "13": "1", "14": "2", "15": "2", "16": "3", "17": "3", "18": "4",
              "19": "4", "20": "5"}

    def setNameRace(self, name, race, gender):
        self.name = name
        self.race = race
        self.gender = gender

    def setTheme(self, theme):
        self.theme = theme

    def setClass(self, cls):
        self.cls = cls

    def setImprovs(self, v):
        self.improvs = v

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
        print(self.attrRoll)
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

    def setSkills(self, data):
        self.skills = data
        # Will buff this up more later as we get closer to actually building our PDF
        #TODO - Finish this section for final CRD 12/24/2018

    def createPDF(self):
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(155, 753, self.name)  # Draw the name on the top
        can.drawString(215, 731, self.race)  # Draw our character race on the sheet
        can.drawString(165, 710, self.gender)  # Draw gender
        can.drawString(20, 730, self.cls)  # Draw Class
        can.drawString(315, 730, self.theme)  # Theme
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("original.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page2 = existing_pdf.getPage(1)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        output.addPage(page2)
        # finally, write "output" to a real file
        outputStream = open("destination.pdf", "wb")
        output.write(outputStream)
        outputStream.close()




