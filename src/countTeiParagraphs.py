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

    '''
    main
    '''

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    body = root.find(prefix+"body")

    count = 0

    page_array = []
    last_page = ""
    uri_map = dict()

    with open(outputpath, 'w', encoding='shift_jis', errors='replace') as f:
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく

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

                        text_sum += text + "<br/>\r\n"

            pages = p.findall(prefix+"pb")
            for page in pages:
                n = page.get("n")
                facs = page.get("facs")
                page_array.append(n)
                last_page = n
                uri_map[n] = facs

            date = p.find(prefix+"date")
            print(str(count)+":\t"+title)
            if date != None:

                # print(str(count)+":\t"+title)

                dateStr = date.get("when")

                start_page = page_array[0]

                media_uri = uri_map[start_page]
                thumb_uri = ""

                canvasId = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/21834/canvas/p"+str(start_page);

                caption = "<a href=\"https://nakamura196.github.io/gozen/mirador?manifest=https://nakamura196.github.io/gozen/data/manifest.json&canvasID="+canvasId+"\">御前落居記録 p."+start_page+"</a>"

                text_sum += "<br/>" + caption

                title = str(count)+": "+title

                line = []
                line.append(title)
                line.append(text_sum)
                line.append(media_uri)
                line.append("") #Media Credit
                line.append("") #Media Caption
                line.append(thumb_uri)

                writer.writerow(line)




            page_array = []
            page_array.append(last_page)

            count += 1


if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml)
