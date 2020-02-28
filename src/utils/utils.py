import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import re
import math
import random

# Jaccard Distance for edge (x,y)
def JD(G,x,y):
    neighs_x = set()
    neighs_y = set()
    try:
        neighs_x = set(G.neighbors(x))
        neighs_y = set(G.neighbors(y))
    except:
        pass

    if len(neighs_x) == 0 or len(neighs_y) == 0:
        return 0
    a = len(neighs_x.intersection(neighs_y))
    b = len(neighs_x.union(neighs_y))
    return a/b

# Create a page rank file from graph with pickle
def PR_file(G, path, a = 0.85):
    pr = nx.pagerank(G, alpha=a)
    pickle.dump(pr,open(path, 'wb'))

# Return Adamic/Adar Index for edge (x,y)
def AdamicAdarIndex(G,x,y):
    neighs_x = set()
    neighs_y = set()
    try:
        neighs_x = set(G.neighbors(x))
        neighs_y = set(G.neighbors(y))
    except:
        pass
    inter = neighs_x.intersection(neighs_y)
    sum = 0
    if len(inter) > 0:
        for com in inter:
            deg = G.degree[com]
            sum = sum + (1/math.log(deg))
    return sum

# Create a HITS file from graph with pickle
def HITS(G, path):
    hits = nx.hits(G, max_iter=500, tol=1e-08, nstart=None, normalized=True)
    pickle.dump(hits,open(path, 'wb'))

# Create a category file from '/data/categories' to dictionary with pickle, takes tsv as input
def categories(in_file, out_file):
    with open(in_file) as fp:
        line = fp.readline()
        categories = []
        cat_dict = dict()
        while line:

            splitted = re.split(r'\t+', line)

            # article
            x = splitted[0]
            cat_dict[x] = set()

            # categories of article x
            cat = splitted[1]

            x_cats = cat.split('.')

            for cat_i in x_cats:
                x_cat = cat_i.split('\n')[0]

                if x_cat in categories:
                    temp = cat_dict[x]
                    temp.add(categories.index(x_cat))
                    cat_dict[x] = temp
                else:
                    temp = cat_dict[x]
                    temp.add(len(categories))
                    cat_dict[x] = temp
                    categories.append(x_cat)
            line = fp.readline()
        pickle.dump(cat_dict,open(out_file, 'wb'))
        pickle.dump(categories,open('../data/numberToCategoryNameList.pkl', 'wb'))

#categories('../data/categoriesDecoded.tsv', '../data/getCategoryFromLinkDict.pkl')

# Create X vector (tuple) for edge (x,y) in graph G
def create_X(G,x,y, categories_dict, pr, hits):
    jd = JD(G,x,y)
    aa = AdamicAdarIndex(G,x,y)

    cats_x = 0
    cats_y = 0
    no_comm = 0
    try:
        cats_x = categories_dict[x]
        cats_y = categories_dict[y]
        no_comm = len(cats_x.intersection(cats_y))
    except:
        pass
    
    pr_x = 0
    pr_y = 0
    try:
        pr_x = pr[x]
        pr_y = pr[y]
    except:
        pass

    hits_x = 0
    hits_y = 0

    try:
        hits_x = hits[0][x]
        hits_y = hits[0][y]
    except:
        pass
    return no_comm, jd, aa, pr_x, pr_y, hits_x, hits_y
