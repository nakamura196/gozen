import xml.etree.ElementTree as ET
import json
import csv
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
    outputpath = inputpath+"_sjis.csv"

    omeka_id = "21834"
    manifest_filename = "kiroku.json"
    filename = "御前落居記録"

    '''
    main
    '''

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    prefix2 = "{http://www.tei-c.org/ns/1.0}"
    prefix3 = "{http://www.w3.org/XML/1998/namespace}"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    body = root.find(prefix+"body")

    count = 1

    imgMap = dict()

    with open(outputpath, 'w', encoding='shift_jis', errors='replace') as f:
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく


        pages = body.findall(prefix+"pb")
        for page in pages:
            n = page.get("n")
            facs = page.get("facs")
            imgMap[int(n)] = facs

        divs = body.findall(prefix2+"div")
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
                text += "<br/>\r\n"

            canvasId = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+omeka_id+"/canvas/p"+str(page);

            caption = "<a href=\"https://nakamura196.github.io/gozen/mirador?manifest=https://nakamura196.github.io/gozen/data/"+manifest_filename+"&canvasID="+canvasId+"\">"+filename+" p."+str(page)+"</a>"

            text += "<br/>"+caption

            media = imgMap[page]
            thumb = media.replace(",600", ",200")

            line = []
            line.append(title)
            line.append(text)
            line.append(media)
            line.append("") #Media Credit
            line.append("") #Media Caption
            line.append(thumb)

            writer.writerow(line)

            count += 1

if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml)
