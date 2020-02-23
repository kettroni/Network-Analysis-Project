import re
from urllib.parse import unquote

def decodingfromUTF8():
    with open('./wikispeedia_paths-and-graph/links.tsv') as fp:
        line = fp.readline()
        i = 1
        while i <= 12:
            line = fp.readline()
            i = i+1

        while line:
            splitted = re.split(r'\t+', line)
            splits = []
            for split in splitted:
                d = unquote(split)
                splits.append(d)
            f = open("decoded.tsv", "a")
            f.write(str(splits[0]) + "\t" + str(splits[1]))
            f.close()
            line = fp.readline()


decodingfromUTF8()
