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
wf = Workflow('Sandia Fracture Challenge 3', automate_execution=False)         # name
storage=Storage(proceduresLibrary)                                  # folder or database

# body of workflow: this changes
sample = Sample('AM_NA_05')

wf.step1 = step(storage, sample, 'polish', {}, run_after_init=True)   #define step and link to storage for procedures

wf.step2 = step(storage, sample, 'light microscopy', {}, run_after_init=True)

wf.step3 = step(storage, sample, 'tensile test', {}, run_after_init=True)

wf.step4 = step(storage, sample, 'light microscopy', {}, run_after_init=True)

wf.step5a = step(storage, sample, 'sem', {'voltage':'30'}, run_after_init=True)

wf.step5b = step(storage, sample, 'sem', {'voltage':'30'}, run_after_init=True)

wf.step1 >> wf.step2 >> wf.step3 >> wf.step4 >> wf.step5a >> wf.step5b
wf.starting_nodes = [wf.step1]

# footer, always the same
print('Output:\n  ','\n   '.join([f"{k}: {v}" for k, v in list(wf.outputs.to_value_dict().items())]))
wf.draw().render(filename="io_demo", format="png", cleanup=True) #plot to file

# {"type":"common-workflow-description", "version":1.0, "shasum":"d5d8342b266851e28919e69039918d2c2a9ca4f2"}