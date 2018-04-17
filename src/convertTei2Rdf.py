import xml.etree.ElementTree as ET
from rdflib import Graph
from rdflib import URIRef, Literal
from rdflib.namespace import DC
import argparse
import sys

def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'path_to_xml',
        action='store',
        type=str,
        help='Ful path to tei file.')

    return parser.parse_args(args)

def main(path_to_xml):

    inputpath = path_to_xml
    outputpath = inputpath+".rdf"

    omeka_id = "21834"
    name = "kiroku"

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    body = root.find(prefix+"body")

    page_array = []

    g = Graph()

    count = 0

    ps = body.findall(prefix+"p")

    for p in list(ps):

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
        dateText = ""
        if date != None:
            dateText = date.text

        print(str(count)+":\t"+title)

        dateStr = ""
        if date != None:
            dateStr = date.get("when")

        s = URIRef("http://example.org/"+name+"/"+'{0:03d}'.format(count))

        title = str(count)+": "+title

        start_page = page_array[0]

        canvasId = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+omeka_id+"/canvas/p"+str(start_page);

        caption = "https://nakamura196.github.io/gozen/mirador?manifest=https://nakamura196.github.io/gozen/data/"+name+".json&canvasID="+canvasId

        url = URIRef(caption)

        if count != 0:

            g.add((s, DC.title, Literal(title)))
            g.add((s, DC.description, Literal(text_sum)))
            if dateStr != "":
                g.add((s, DC.date, Literal(dateStr)))
            g.add((s, DC.relation, url))
            g.add((s, DC.subject, Literal(name)))

        count += 1

    f = open(outputpath, "wb")
    f.write(g.serialize(format='xml'))
    f.close()


if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml)
