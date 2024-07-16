# common_workflow_description
## A mockup of a common format to describe experimental and numerical workflows

Shows how a format could look like that can be used for experiments and simulations.

## Folders
- base-folder: here we put some exp. and num. workflows with .py ending
- procedures: folder with experimental procedures and an index of it. This is like a library of recipes
- tk_based_lib: a simple TK-inter based lib to execute


## Advantage for workflow: sem.py
- workflow can include experiments (as shown) as well as data-analytics and simulations (as per usual)
- workflow body is easy and allows python's flexibility
  - workflow head is always the same
- procedures of each step and sample can be altered
- since .py is a text file, workflows can be:
  1. generated by computer
  2. compared by computer
  3. version controlled by computer

## Advantage of the implementation: tk_based_lib:
- procedures are based on common markdown format
  - only addition is variables/substitution which is copied from reStructured text
  - that addition is extended by the |variable|default| nomenclature, see "sem.md"
- has no python requirements
- creates log file
- creates shasum of procedures so one knows if the underlying procedure changed
- shows message to user and asks for input
- other people can inherit/extend the functionality of storage and sample based on their software (PASTA, pyiron)
  - workflow stays constant and can be exchanged between different systems

## How to start program?
Install and setup conda and start basic example
``` bash
git clone git@git.rwth-aachen.de:nfdi-matwerk/ta-wsd/common_workflow_description.git
cd common_workflow_description/
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
eval "$(/home/steffen/.miniforge3/bin/conda shell.bash hook)"
conda install -c conda-forge pyiron_workflow
python sem.py
```

## TODO:
- discuss with Sarath
  - no jupyter (for now) lets do the comparison as direct as possible
  - sem.py is a suggestion for the common example
  - can we update to the latest version of pyiron-wf?
- let's have also an numerical example
- let's have a combined example
- can we find better names for things: storage, smartSample
- TK part is not ideal, don't know how to fix easily: one window that gets updated
- more experimental procedures
- current version of pyiron workflow is delayed running: define all steps; run them
  better: run steps immediately
- pyiron-workflow 0.9.1 still has sooooo many requirements, incl. mpi-stuff
  - should we have a feature-poor version that has no requriements as part of the tk-based-lib
  - if people need more features: use pyiron

