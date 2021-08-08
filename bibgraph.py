import sys
import datetime

import bibtexparser
import networkx as nx
import pydot
from collections import Counter

from subprocess import call

TAG_MAP = {
        't': 'toread',
        'm': 'mapped',
        'i': 'inprogress',
        'r': 'read'}

def unpack(citationString):
    keys_cited = [s.strip() for s in citationString.split(',')]
    return keys_cited


def quick_stats(bibtex):
    stats = Counter()
    for key, entry in bibtex.entries_dict.items():
        tag = entry.get('tags')
        if tag:
            newtag = ''
            for t in tag:
                newtag += TAG_MAP[t] + ' '
            tag = newtag
        stats[tag] += 1
    return stats

# The following are the node classes
#   r, i, t - read, in progress, to read
#   m - maps/includes all (relevant) work citing this node at the time of writing


if __name__ == '__main__':
    
    bibfile = sys.argv[1]
    print(f"Bibfile is {bibfile}")

    with open(bibfile) as bibtex_file:
        bibtex = bibtexparser.load(bibtex_file)

    stats = quick_stats(bibtex)
    for k,v in stats.items():
        print("{0:>5} --> {1:}".format(v, k))

    citations = {}
    tags = {}

    for key, entry in bibtex.entries_dict.items():
        cites = entry.get('cites')
        if cites:
            citations[key] = unpack(cites)
        t = entry.get('tags')
        if t:
            tags[key] = t

    G = nx.DiGraph()
    for key, entry in citations.items():
        for cit in entry:
            G.add_edge(key, cit)

    # https://github.com/kavonjon/bibgraph/ 
    ## fix for networkX 2
    #pydot_G = nx.drawing.nx_pydot.to_pydot(G)

    pydot_G = nx.nx_pydot.to_pydot(G)
    for node in pydot_G.get_nodes():
        t = node.get_name()
        if t and tags.get(t):
            node.set('nodetype', tags.get(t))

    pydot_G.set('rankdir', 'LR')
    pydot_G.set('style', 'dashed')
    pydot_G.write('bib.dot')

    yymmddhhss   = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    png_filename = "bib_" + yymmddhhss + ".png"
    pdf_filename = "bib_" + yymmddhhss + ".pdf"

    call(["gvpr -c -f filter.gvpr bib.dot > bib_nice.dot"], shell=True)
    # create png from bib_nice.dot
    call(["ccomps -x bib_nice.dot | dot | gvpack -array1 | neato -Tpng -n2 -o png_filename"], shell=True)
    # create pdf from bib_nice.dot
    call(["ccomps -x bib_nice.dot | dot | gvpack -array1 | neato -Tpdf -n2 -o pdf_filename"], shell=True)