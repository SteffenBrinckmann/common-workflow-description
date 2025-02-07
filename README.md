# common_workflow_description
This is a temporary copy of the rwth-gitlab repo: it allows easier communication with external partners.

## A mockup of a common format to describe experimental and numerical workflows

Shows how a format could look like that can be used for experiments and simulations.

## Folders
- workflows: here we put some exp. and num. workflows with .py ending
- procedures: folder with experimental procedures and an index of it. This is like a library of recipes for experimentaliest
- tk_based_lib: a simple TK-inter based lib


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
- if pyiron-workflow is not found: uses minimalistic workflow engine
  - uses the same nomenclature as pyiron-workflow
  - not as feature-rich: drawing, scheduling, ...
  - has no dependency and just-runs code
- creates log file of the experiments
- creates shasum of procedures so one knows if the underlying procedure changed
- shows message to user and asks for input
- other people can inherit/extend the functionality of storage and sample based on their software (PASTA, pyiron)
  - workflow stays constant and can be exchanged between different systems


## How to start program?
Install and setup conda
``` bash
git clone git@git.rwth-aachen.de:nfdi-matwerk/ta-wsd/common_workflow_description.git
cd common_workflow_description/
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

Start conda environment, install pyiron, and start workflow
``` bash
eval "$(/home/steffen/.miniforge3/bin/conda shell.bash hook)"
conda install -c conda-forge pyiron_workflow
python workflow_example.py
```
## Misc notes
- S.Stier uses "sample.polish" notation

## TODO: Next steps
- Data classes
- Allow for more parameters per line
- Allow for multiple files uploaded
