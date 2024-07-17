# head of workflow: always the same
import sys
from pathlib import Path
from pyiron_workflow import Workflow

# paths for these examples to work in this folder structure
sys.path.append(str(Path(__file__).parent.parent))
from tk_based_lib.storage import Storage, step
from tk_based_lib.sample import Sample
proceduresLibrary = Path(__file__).parent.parent/'procedures'

wf = Workflow('example_workflow')         #name
storage=Storage(proceduresLibrary)

# body of workflow
sample = Sample('FeAl')

wf.step1 = step(storage, sample, 'polish', {})   #define step and link to storage for procedures

wf.step2 = step(storage, sample, 'light microscopy', {})

wf.step3 = step(storage, sample, 'sem', {'voltage':'30'})

# footer, always the same
out = wf.run()
print('Output:\n  ','\n   '.join([str(i) for i in list(out.values())]))

# wf.draw().render(view=True)               #plot to screen (creating pdf->viewer)
wf.draw().render(filename="io_demo", format="png") #plot to file
