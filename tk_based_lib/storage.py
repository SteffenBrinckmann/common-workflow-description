""" Storage for procedures """
import re, logging, json, hashlib
from typing import Union, Any
from pathlib import Path
from pyiron_workflow.function import single_value_node
from .sample import Sample
from .tk_inter import window

class Storage():
    """Storage for procedures"""

    def __init__(self, procedures) -> None:
        """Storage of procedures

        Args:
          procedures (): location or list of procedures to choose from
        """
        self.procedures: dict[str, Union[str, Path]] = {}
        if isinstance(procedures, dict):
            self.addProcedures(procedures)
        if isinstance(procedures, Path):
            self.addProcedureDirectory(procedures)
        logging.basicConfig(
            filename="workflow.log",
            level=logging.INFO,
            datefmt="%m-%d %H:%M:%S",
            format="%(asctime)s|%(levelname)s:%(message)s",
        )
        logging.info("Start workflow")


    def addProcedures(self, procedures: dict[str, Union[str, Path]]) -> None:
        """Add procedures to local copy

        Args:
          procedures (dict): dictionary of procedures (text), or files-of-procedures
        """
        for key, value in procedures.items():
            if isinstance(value, str):
                if Path(value).exists():
                    self.procedures[key] = Path(value)
                    continue
            self.procedures[key] = value
        return


    def addProcedureDirectory(self, path: Path) -> None:
        """Add directory with procedures to local copy
        - index.json file in that directory defines names

        Args:
          path (Path): directory with procedure files
        """
        procedures = json.load(open(path / "index.json", encoding="utf-8"))
        for key, value in procedures.items():
            if (path / value).exists():
                self.procedures[key] = path / value
                continue
            self.procedures[key] = value
        return


    def listParameters(self, name: str) -> dict[str, str]:
        """list all the parameters in this procedure

        Args:
          name (str): name of procedure

        Returns:
          dict: key,default pairs of parameters
        """
        text = self.getText(name)
        params = re.findall(r"\|\w+\|.*\|", text)
        return {i.split("|")[1]: i.split("|")[2] for i in params}


    def getText(self, name: str) -> str:
        """get text of this procedure

        Args:
          name (str): name of procedure

        Returns:
          str: its text
        """
        if name not in self.procedures:
            raise ValueError("Name of step not in procedures:", name)
        procedure = self.procedures[name]
        if isinstance(procedure, str):
            text = procedure
        else:
            with open(procedure, encoding="utf-8") as fIn:
                text = fIn.read()
        return text




@single_value_node()
def step(storage:Storage, sample: Sample, name: str, param: dict[str, Any] = {}):
    """Render in TkInter

    Args:
      sample (Sample): sample to do step on
      name (str): name of procedure
      param (dict): parameter to change from default procedure

    Returns:
      Sample: changed sample / child sample
      str: file name of result
      dict: metadata collected during step
    """
    text = storage.getText(name)
    m = hashlib.sha256()
    m.update(text.encode("utf-8"))
    shasum256 = m.hexdigest()
    if param is not None:
        for key, value in param.items():
            text = re.sub(f"\|{key}\|.+\|", value, text)
    text = re.sub("\|\w+\|(.+)\|", r"\1", text)
    text = f"# Execute the following action with sample: {sample.name}\n{text}"
    logging.info(
        f"Start step sample:{sample.name}  procedure-name:{name}  sha256:{shasum256}  "
        f"parameters:\n{json.dumps(param, indent=2)}"
    )
    paramAll = storage.listParameters(name)
    fileName, metadata = window(text, paramAll, param)
    logging.info(f"End step ")
    return [sample, fileName, metadata]
