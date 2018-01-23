# lingpy-interface
An interface and extension to LingPy: Python library for quantitative tasks in historical linguistics.

Also in this repository are files for work presented in "An Interface and Case Studies for Automatic Cognate Detection Methods" (link forthcoming), a senior linguistics thesis at Swarthmore College.

## Files
- ABVDStudy.ipynb and SlavicStudy.ipynb contain code run for case studies in the thesis
- workflow.py contains deprecated code from LingPy 2.5, as reference
- input/ contains any input files used in the iPython notebooks or other scripts
- all scripts and notebooks are hardcoded to write files to output/
- result_files/ contains files with results discussed in the thesis

## Tools
- swadesh_scraper.py
- interface.ipynb

## User Instructions

Start with Anaconda installation instructions for your system at [the Anaconda documentation link](https://docs.anaconda.com/anaconda/install/).

Once Anaconda is installed, you can use pip to install new packages into the Anaconda Python distribution. Install LingPy according to the instructions at its [repository, here](https://github.com/lingpy/lingpy). To install with pip, open a terminal and type in the following:
```bash
$ pip install lingpy
```

Then, to install the code in this repository, type:
```bash
$ git clone https://github.com/kjcollins/lingpy-interface.git
$ cd lingpy-interface
```

To use the interface in interface.ipynb, make sure you're in the lingpy-interface directory, and run:
```bash
$ jupyter notebook
```

This creates a local server for Jupyter/iPython notebooks. It should open automatically with your default browser.

Start exploring the interface! Any .ipynb files can be viewed and edited from the server's directory listing. The other tools and files in this repository can be viewed using the notebook server, or with any text editor or IDE as desired.


To close the notebook server, type command-C (for MacOS, or whatever kills a process on your system).
