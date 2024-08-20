# head of workflow: always the same
from pathlib import Path
from tk_based_lib.storage import Storage, step
from tk_based_lib.sample import Sample
try:
    from pyiron_workflow import Workflow
except ImportError:
    from tk_based_lib.workflow import Workflow

# start code
proceduresLibrary = Path(__file__).parent.parent/'procedures'
wf = Workflow('example_workflow', automate_execution=False)         # name
storage=Storage(proceduresLibrary)                                  # folder or database

# body of workflow: this changes
sample = Sample('FeAl')

wf.step1 = step(storage, sample, 'polish', {}, run_after_init=True)   #define step and link to storage for procedures

wf.step2 = step(storage, sample, 'light microscopy', {}, run_after_init=True)

wf.step3 = step(storage, sample, 'sem', {'voltage':'30'}, run_after_init=True)

try:
    wf.step1 >> wf.step2 >> wf.step3
except:
    pass
wf.starting_nodes = [wf.step1]

# footer, always the same
out = wf.run()
print('Output:\n  ','\n   '.join([str(i) for i in list(out.values())]))

# wf.draw().render(view=True)               #plot to screen (creating pdf->viewer)
wf.draw().render(filename="io_demo", format="png", cleanup=True) #plot to file
