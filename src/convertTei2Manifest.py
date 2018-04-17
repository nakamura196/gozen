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

    return parser.parse_args(args)

def main(path_to_xml, path_to_manifest):

    f = open(path_to_manifest, "r") #ここが(1)
    manifest = json.load(f) #ここが(2)
    f.close()

    inputpath = path_to_xml
    omeka_id = "21835"

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    body = root.find(prefix+"body")

    count = 0

    page_array = []
    last_page = ""
    uri_map = dict()

    structures = []

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
            last_page = n
            uri_map[n] = facs

        date = p.find(prefix+"date")
        dateText = ""
        if date != None:
            dateText = date.text
        # if date != None:

        print(str(count)+":\t"+title)

        dateStr = ""
        if date != None:
            dateStr = date.get("when")
            dateStr = "（"+dateStr+"）"

        if count != 0:

            st = dict()
            structures.append(st)

            st["canvases"] = []
            for n in page_array:
                st["canvases"].append("https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+omeka_id+"/canvas/p"+n)
            st["@id"] = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+omeka_id+"/c"+str(count)
            st["@type"] = "sc:Range"
            st["label"] = str(count)+": "+dateText+dateStr+": " + title

        count += 1


        page_array = []
        page_array.append(last_page)

    manifest["structures"] = structures

    fw = open(path_to_manifest,'w')
    json.dump(manifest,fw,indent=4)
    fw.close()

if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml,
        args.path_to_manifest)
