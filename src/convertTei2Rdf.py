import xml.etree.ElementTree as ET
from rdflib import Graph
from rdflib import URIRef, Literal
from rdflib.namespace import DC

'''
paramter
'''

inputpath = '../data/kiroku.xml'
outputpath = inputpath+".rdf"

'''
main
'''

prefix = ".//{http://www.tei-c.org/ns/1.0}"

tree = ET.parse(inputpath)
root = tree.getroot()

body = root.find(prefix+"body")


g = Graph()

count = 1

for p in list(body):

    text_sum = ""

    title = ""

    lines = p.findall(prefix+"line")

    if len(lines) > 0:

        for i in range(0, len(lines)):
            line = lines[i]
            if line.text != None:
                text = line.text
                if i == 0:
                    title = text
                    if title == "（花押）":
                        title = lines[i+1].text

                text_sum += text + "\r\n"

    date = p.find(prefix+"date")
    if date != None:

        print(str(count)+":\t"+title)

        dateStr = date.get("when")

        s = URIRef("http://example.org/"+'{0:02d}'.format(count))

        g.add((s, DC.title, Literal(title)))
        g.add((s, DC.description, Literal(text_sum)))
        g.add((s, DC.date, Literal(dateStr)))

        count += 1

f = open(outputpath, "wb")
f.write(g.serialize(format='xml'))
f.close()
