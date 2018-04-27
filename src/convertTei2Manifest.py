import xml.etree.ElementTree as ET
import json
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
        'path_to_manifest',
        action='store',
        type=str,
        help='Ful path to manifest file.')

    parser.add_argument(
        'omeka_id',
        action='store',
        type=str,
        help='omeka id.')

    return parser.parse_args(args)

def main(path_to_xml, path_to_manifest, omeka_id):

    f = open(path_to_manifest, "r") #ここが(1)
    manifest = json.load(f) #ここが(2)
    f.close()

    inputpath = path_to_xml

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    prefix2 = "{http://www.tei-c.org/ns/1.0}"
    prefix3 = "{http://www.w3.org/XML/1998/namespace}"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    body = root.find(prefix+"body")

    count = 1

    divs = body.findall(prefix+"div")

    structures = []

    for div in divs:

        page_array = []

        ss = div.findall(prefix+"s")

        for s in ss:
            attrs = s.attrib[prefix3+"id"].split("_")
            page = int(attrs[0][3:])
            if page not in page_array:
                page_array.append(page)

        title = ss[0].text

        if title.find("花押") > -1:
            title = ss[1].text
            if title.find("花押") > -1:
                title = ss[2].text

        title = str(count)+": "+title

        st = dict()
        structures.append(st)

        st["canvases"] = []
        for n in page_array:
            st["canvases"].append("https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+omeka_id+"/canvas/p"+str(n))
        st["@id"] = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+omeka_id+"/c"+str(count)
        st["@type"] = "sc:Range"
        st["label"] = title

        count += 1

    manifest["structures"] = structures

    fw = open(path_to_manifest+"_added.json",'w')
    json.dump(manifest,fw,indent=4)
    fw.close()

if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml,
        args.path_to_manifest,
        args.omeka_id)
