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

    parser.add_argument(
        'omeka_id',
        action='store',
        type=str,
        help='omeka id')

    parser.add_argument(
        'name',
        action='store',
        type=str,
        help='name')

    return parser.parse_args(args)

def main(path_to_xml, omeka_id, name):

    inputpath = path_to_xml
    outputpath = inputpath+".rdf"

    manifest_filename = "hosyo.json"
    filename = "御前落居奉書"

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    prefix2 = "{http://www.tei-c.org/ns/1.0}"
    prefix3 = "{http://www.w3.org/XML/1998/namespace}"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    body = root.find(prefix+"body")

    g = Graph()

    count = 1

    divs = body.findall(prefix+"div")

    for div in divs:

        ss = div.findall(prefix+"s")

        attrs = ss[0].attrib[prefix3+"id"].split("_")
        page = int(attrs[0][3:])

        title = ss[0].text

        if title.find("花押") > -1:
            title = ss[1].text
            if title.find("花押") > -1:
                title = ss[2].text

        title = str(count)+": "+title

        text = ""
        for s in ss:
            for ite in s.itertext():
                text += ite
            text += "\r\n"

        canvasId = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+omeka_id+"/canvas/p"+str(page);

        caption = "https://nakamura196.github.io/gozen/mirador?manifest=https://nakamura196.github.io/gozen/data/"+manifest_filename+"&canvasID="+canvasId

        date = div.find(prefix+"date")
        dateText = ""
        if date != None:
            dateText = date.get("when")

        s = URIRef("http://example.org/"+name+"/"+'{0:03d}'.format(count))

        url = URIRef(caption)

        g.add((s, DC.title, Literal(title)))
        g.add((s, DC.description, Literal(text)))
        if dateText != "":
            g.add((s, DC.date, Literal(dateText)))
        g.add((s, DC.relation, url))
        g.add((s, DC.subject, Literal(name)))

        count += 1


    f = open(outputpath, "wb")
    f.write(g.serialize(format='xml'))
    f.close()


if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml,
        args.omeka_id,
        args.name)
