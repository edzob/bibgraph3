# bibgraph

`bibgraph` builds a citation graph from an _annotated_ bibtex file.



## Build a graph
Bibgraph expects to find the following optional fields:

1. `cites` on every entry to be added to the graph; 
   this contains a list of (keys of) entries cited by that entry
2. `tags` (optional) marking the status of that document; 
   the following tags are supported:
   1. `i` - in progress
   2. `t` - to read
   3. `r` - read
   4. `m` - append this tag to each entry you have fully mapped
      (i.e. checked all interesting references and 
      works that refer to it and added them to the bibliography graph)

This means you have to add these two fields 
(_By hand_)
if you want to see a graph.

An example entry for a paper citing `zhang2009fpga` 
which is `in progress` and `mapped`:

```
@inproceedings{kestur2012towards,
   title = {{Towards a universal FPGA matrix-vector multiplication architecture}},
   author = {Kestur, Srinidhi and Davis, John D and Chung, Eric S},
   booktitle = FCCM,
   pages = {9--16},
   year = {2012},
   cites = {zhang2009fpga},
   tags = {im}
}
```

## Suggested Workflow
1. Pick a paper
2. Set it as `t`
3. Add it to the bibliography graph
4. Add all _interesting_ references (based on title and context)
5. Add all work citing the paper 
(e.g. using Google Scholar's _Cited By_ feature)
6. Set is as `m`
7. Play some _Mass Effect_...

## Requires
1. Installed version of Python 3. This script is tested with version 3.8
1. Clone reposiitory
```bash
# git clone git@github.com:paul-g/bibgraph.git;
git clone git@github.com:lissonc/bibgraph3.git;
```

1. Install graphviz on linux
```bash
sudo apt-get update;
sudo apt-get install graphviz;
```
   1. Install graphvix on Mac
```bash
brew install graphviz;
```
1. Install Python helper files: 
[Pydot](https://github.com/pydot/pydot), 
[Bibtexparser](https://github.com/sciunto-org/python-bibtexparser), 
[networkx](https://github.com/networkx/networkx)
```bash
python3 -m pip install --upgrade pip;
python3 -m pip install pydot bibtexparser networkx;
python3 -m pip freeze| grep pydot; 
python3 -m pip freeze| grep bibtexparser;
python3 -m pip freeze| grep networkx;
```

## Helpful hints
### Bibtex vs BibLaTex
Bibgraph3 relies on bibtexparser which only supports BibTeX entry types; not the full set available in BibLaTeX. 

For example: @techreport is supported while @report is not. 
This can be a pain to figure out because it fails silently.
### Cites
The script can read bibtex entries without cites, 
and correctly not put this in a graph.

### Tags
The script can read bibtex entries without tags.


## Running

`python3 bibgraph.py /path/to/your/bibliography.bib`

This produces a `bib.png` and a `bib.pdf` file a the bibliography graph like the one below.

![Example bibgraph](/bib.png?raw=true "Example bibgraph")

## Contributors
- Orginal script - https://github.com/paul-g/bibgraph/
- Fork into python3 script - https://github.com/lissonc/bibgraph3
- Fork into minor adjustments - https://github.com/edzob/bibgraph3
