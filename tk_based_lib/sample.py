""" Sample with a name """
class Sample:
    """ Sample with a name """
    def __init__(self, name: str) -> None:
        """Sample with a name: most basic sample

        Args:
          name (str): human readable name of sample
        """
        self.name = name

    def __repr__(self) -> str:
        return f'Name: {self.name}'

    def print(self) -> None:
        """ Print sample name to screen """
        print(f'Name: {self.name}')
