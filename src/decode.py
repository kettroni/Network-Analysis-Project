import re
from urllib.parse import unquote
import pickle

def decodingfromUTF8(filepath, firstrow, name):
    with open(filepath) as fp:
        line = fp.readline()
        i = 1
        while i <= firstrow-1:
            line = fp.readline()
            i = i+1

        while line:
            splitted = re.split(r'\t+', line)
            splits = []
            for split in splitted:
                d = unquote(split)
                splits.append(d)
            f = open(name, "a")
            f.write(str(splits[0]) + "\t" + str(splits[1]))
            f.close()
            line = fp.readline()

with open('../data/getCategoryFromLinkDict.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)

with open('../data/numberToCategoryNameList.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)
    print(len(data))
#decodingfromUTF8('./wikispeedia_paths-and-graph/categories.tsv', 14, 'categoriesDecoded.tsv')
