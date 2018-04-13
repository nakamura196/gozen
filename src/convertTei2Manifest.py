import xml.etree.ElementTree as ET
import json

'''
paramter
'''

inputpath = '../data/kiroku.xml'

'''
main
'''

prefix = ".//{http://www.tei-c.org/ns/1.0}"

tree = ET.parse(inputpath)
root = tree.getroot()

body = root.find(prefix+"body")

count = 1

page_array = []
last_page = ""
uri_map = dict()

structures = []

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

    pages = p.findall(prefix+"pb")
    for page in pages:
        n = page.get("n")
        facs = page.get("facs")
        page_array.append(n)
        last_page = n
        uri_map[n] = facs

    date = p.find(prefix+"date")
    if date != None:

        print(str(count)+":\t"+title)

        dateStr = date.get("when")

        st = dict()
        structures.append(st)

        st["canvases"] = []
        for n in page_array:
            st["canvases"].append("https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/21834/canvas/p"+n)
        st["@id"] = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/21834/c"+str(count)
        st["@type"] = "sc:Range"
        st["label"] = dateStr + " : " + title

        count += 1


    page_array = []
    page_array.append(last_page)

print(structures)
