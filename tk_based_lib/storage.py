""" Storage for procedures """
import hashlib
import json
import logging
import re
from typing import Union, Any, Optional
from pathlib import Path
# from pyiron_workflow import Workflow
from .workflow import Workflow
from .sample import Sample
from .tk_inter import main_window

class Storage():
    """Storage for procedures"""

    def __init__(self, procedures) -> None:
        """Storage of procedures

        Args:
          procedures (): location or list of procedures to choose from
        """
        self.procedures: dict[str, Union[str, Path]] = {}
        if isinstance(procedures, dict):
            self.add_procedures(procedures)
        if isinstance(procedures, Path):
            self.add_procedure_directory(procedures)
        logging.basicConfig(
            filename="workflow.log",
            level=logging.INFO,
            datefmt="%m-%d %H:%M:%S",
            format="%(asctime)s|%(levelname)s:%(message)s",
        )
        logging.info("Start workflow")


    def add_procedures(self, procedures: dict[str, Union[str, Path]]) -> None:
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


    def add_procedure_directory(self, path: Path) -> None:
        """Add directory with procedures to local copy
        - index.json file in that directory defines names

        Args:
          path (Path): directory with procedure files
        """
        with open(path / "index.json", encoding="utf-8") as file_input:
            procedures = json.load(file_input)
        for key, value in procedures.items():
            if (path / value).exists():
                self.procedures[key] = path / value
                continue
            self.procedures[key] = value


    def list_parameters(self, name: str) -> dict[str, str]:
        """list all the parameters in this procedure

        Args:
          name (str): name of procedure

        Returns:
          dict: key,default pairs of parameters
        """
        text = self.get_text(name)
        params = re.findall(r"\|\w+\|.*\|", text)
        return {i.split("|")[1]: i.split("|")[2] for i in params}


    def get_text(self, name: str) -> str:
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
            with open(procedure, encoding="utf-8") as file_input:
                text = file_input.read()
        return text




@Workflow.wrap.as_function_node("y")
def step(storage:Storage, sample: Sample, name: str, param: Optional[dict[str, Any]] = None):
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
    if param is None:
        param = {}
    text = storage.get_text(name)
    m = hashlib.sha256()
    m.update(text.encode("utf-8"))
    shasum256 = m.hexdigest()
    if param is not None:
        for key, value in param.items():
            text = re.sub(r"\|{key}\|.+\|", value, text)
    text = re.sub(r"\|\w+\|(.+)\|", r"\1", text)
    text = f"# Execute the following action with sample: {sample.name}\n{text}"
    logging.info("Start step sample:{%s}  procedure-name:{%s}  sha256:{%s}  parameters:\n{%s}",
                 sample.name, name, shasum256, json.dumps(param, indent=2))
    parameter_all = storage.list_parameters(name)
    file_name, metadata = main_window(text, parameter_all, param)
    logging.info("End step ")
    return [sample, file_name, metadata]
