from PyPDF2 import PdfFileWriter, PdfFileReader
import io, os, json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

cwd = os.getcwd()

charName = "Damarius"
race = 'Lashuntas'
gender = "Male"
charClass = "envoy"
charTheme = "Ace Pilot"
skills = {"acro":{"tot": "7", "rnk": "1", "bon": "3", "abm": "4"}, "athl":{"tot": "5", "rnk": "1", "bon": "3", "abm": "1"}}

with open(cwd+'/app/json/skills.json', 'rb') as f:
    mSkills = json.load(f)

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(155, 753, charName)
can.drawString(215, 731, race)
can.drawString(165, 705, gender)
can.drawString(20, 730, charClass)
can.drawString(315, 730, charTheme)
# Draw ability scores
can.drawString(95, 620, '10') #Str
can.drawString(142, 620, '+1') #Str Mod
can.drawString(95, 599, '10') #DEX
can.drawString(142, 599, '+1') #DESX Mod
can.drawString(95, 578, '10') #CON
can.drawString(142, 578, '+1') #CON Mod
can.drawString(95, 556, '10') #INT
can.drawString(142, 556, '+1') #INT Mod
can.drawString(95, 535, '10') #WIS
can.drawString(142, 535, '+1') #WIS Mod
can.drawString(95, 514, '10') #CHA
can.drawString(142, 514, '+1') #CHA Mod

can.drawString(256.5, 483, "11") #Draw skill levels
#This writes which skills are class skills based on user selected class
for s in mSkills:
    if charClass in mSkills[s]['class']:
        x = float(mSkills[s]["pos"]["x"])
        y = float(mSkills[s]["pos"]["y"])
        can.drawImage('10003.png', x, y, 10, 8,
                      mask=[255, 255, 255, 255, 255, 255])
    nm = mSkills[s]
    #Total First
    can.drawString(nm['pos']['xTot'], nm['pos']['yTot'], "0")
    #Ranks
    can.drawString(nm['pos']['xRnk'], nm['pos']['yRnk'], "0")
    #Bonus
    can.drawString(nm['pos']['xBon'], nm['pos']['yBon'], "0")
    #Ability Mod
    can.drawString(nm['pos']['xAbm'], nm['pos']['yAbm'], "0")
can.save()

#move to the beginning of the StringIO buffer
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
outputStream = open(cwd+ "/app/destination.pdf", "wb")
output.write(outputStream)
outputStream.close()

