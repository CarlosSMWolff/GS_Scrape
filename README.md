# Google Scholar Scraping Tools


This repository provides tools for scraping publication data from Google Scholar and generating formatted LaTeX reports. The package includes both Python functions for programmatic use and a command-line interface (CLI) for quick scraping.

---

## Features

- **Google Scholar Scraping**: Extract detailed information about publications, including title, authors, journal, year, citations, and more.
- **Pseudonym Handling**: Unify author names across variations (e.g., "C S Munoz" → "C. Sánchez Muñoz").
- **LaTeX Report Generation**: Automatically generate LaTeX-formatted lists of publications and summary statistics for academic CVs or reports.
- **Command-Line Interface**: Easily scrape Google Scholar data and save it to a CSV file directly from the terminal.
---

## Installation

- Clone this directory
- cd to the current folder `cd GS_Scrape`
- (Recommended) Create a new Python environment and activate it. For instance, using conda, you can create and activate an environment with name `gsscrape`, using Python 3.9, as

```shell
conda create -n gsscrape python=3.9
conda activate gsscrape
```

- Install the `gsscrape` as an editable python package with its dependencies

```shell
pip install -e .
```

In Windows you might need to use a package manager such as Anaconda before
installing the `gsscrape` package.

The details to install conda or a lightweight version called miniconda can be
found below:

- [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
- [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)


## Notebooks

### [example_usage.ipynb](https://github.com/CarlosSMWolff/ParamEst-NN/blob/main/notebooks/1-Trajectories_generation.ipynb)

Notebook with example usage: download the papers as a dataframe and use it to generate a LaTeX snippet for your CV.
