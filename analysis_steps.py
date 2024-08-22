import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
try:
    from pyiron_workflow import Workflow
except:
    from common_workflow_description import Workflow

@Workflow.wrap.as_function_node("y")
def plot_curves(fileName, xLabel, yLabel):
    """
    """
    file = pd.ExcelFile(fileName)
    for idx, sheet in enumerate(file.sheet_names):
        if sheet in ('Measurements'):
            continue
        df = pd.read_excel(file, sheet)
        x = df[xLabel].iloc[1:]
        y = df[yLabel].iloc[1:]
        if idx < 10:
            plt.plot(x,y, label=sheet)
        else:
            plt.plot(x,y)
    plt.legend()
    plt.xlabel(f'{xLabel} [{df[xLabel].iloc[0]}]')
    plt.ylabel(f'{yLabel} [{df[yLabel].iloc[0]}]')
    plt.show()

@Workflow.wrap.as_function_node("y")
def calc_YoungsModulus(fileName, xLabel, yLabel):
    """
    """
    file = pd.ExcelFile(fileName)
    youngsModulii = {}
    for sheet in file.sheet_names:
        if sheet in ('Measurements'):
            continue
        df = pd.read_excel(file, sheet)
        x = np.array(df[xLabel].iloc[1:].astype(float))/100.  #convert from %
        y = np.array(df[yLabel].iloc[1:].astype(float))
        peaks = sp.signal.find_peaks(y, distance=100)[0]
        startUnloading = peaks[peaks>100][0]+10
        valleys = sp.signal.find_peaks(-y, distance=10)[0]
        endUnloading  = valleys[valleys>startUnloading][0]
        fit = np.polyfit(x[startUnloading:endUnloading], y[startUnloading:endUnloading], 1)
        youngsModulii[sheet] = fit[0]/1000.  #to GPa
    Es = np.array(list(youngsModulii.values()))
    print(f"Young's modulus in GPa: average={round(np.mean(Es),2)} std-dev={round(np.std(Es),2)}")

# plot_curves('... NotchedTensileOverallxlsx.xlsx', 'average', 'Axial Aux Load')
# plot_curves('... LongitundinalTensileOverall.xlsx', 'Strain (Gauge0)', 'Engr. Stress')
