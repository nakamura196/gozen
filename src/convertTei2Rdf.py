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

page_array = []

g = Graph()

count = 1

for p in list(body):

    es = list(p)
    if len(es) > 0:
        if es[0].tag == "{http://www.tei-c.org/ns/1.0}pb":
            page_array = []

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
                    if title.find("花押") > -1:
                        title = lines[i+1].text
                        if title.find("花押") > -1:
                            title = lines[i+2].text

                text_sum += text + "\r\n"

    pages = p.findall(prefix+"pb")
    for page in pages:
        n = page.get("n")
        facs = page.get("facs")
        page_array.append(n)

    date = p.find(prefix+"date")
    if date != None:

        print(str(count)+":\t"+title)

        dateStr = date.get("when")

        s = URIRef("http://example.org/"+'{0:02d}'.format(count))

        title = str(count)+": "+title

        start_page = page_array[0]

        canvasId = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/21834/canvas/p"+str(start_page);

        caption = "https://nakamura196.github.io/gozen/mirador?manifest=https://nakamura196.github.io/gozen/data/manifest.json&canvasID="+canvasId

        url = URIRef(caption)

        g.add((s, DC.title, Literal(title)))
        g.add((s, DC.description, Literal(text_sum)))
        g.add((s, DC.date, Literal(dateStr)))
        g.add((s, DC.relation, url))

        count += 1

f = open(outputpath, "wb")
f.write(g.serialize(format='xml'))
f.close()
