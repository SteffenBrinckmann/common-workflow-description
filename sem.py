# head of workflow: always the same
from pathlib import Path
from pyiron_workflow.workflow import Workflow
from tk_based_lib.storage import Storage, step
from tk_based_lib.sample import Sample

wf = Workflow('example_workflow')         #name
folder = Path(__file__).parent.parent/'procedures'

# body of workflow
sample = Sample('FeAl')
storage=Storage(folder)

wf.step1 = step(storage, sample, 'polish', {})   #define step and link to storage for procedures

wf.step2 = step(storage, sample, 'light microscopy', {})

wf.step3 = step(storage, sample, 'sem', {'voltage':'30'})

out = wf.run()

print('Output filename',list(out.values()))

# wf.draw().render(view=True)               #plot to screen (creating pdf->viewer)
wf.draw().render(filename="io_demo", format="png") #plot to file

# here we could use fileName to determine things: data science
# we can also add pyiron code


