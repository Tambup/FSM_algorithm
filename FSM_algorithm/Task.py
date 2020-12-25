from .core import ComportamentalFANetwork


class Task:
    def __init__(self, compFAN):
        self._compFAN = compFAN

    @property
    def compFAN(self) -> ComportamentalFANetwork:
        return self._compFAN

    def build(self, param=None):
        pass
