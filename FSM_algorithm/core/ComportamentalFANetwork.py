from core.ComportamentalFA import ComportamentalFA


class ComportamentalFANetwork():
    def __init__(self, name, CFAs):
        self._name = name
        self._comportamentalFAs = []
        for cfa in CFAs:
            self._comportamentalFAs.append(ComportamentalFA(name=cfa["name"],
                                           states=cfa["state"]))

    @property
    def name(self):
        return self._name

    @property
    def comportamentalFAs(self):
        return self._comportamentalFAs

    def check(self):
        if len(self._comportamentalFAs) < 1:
            return False

        for compFA in self._comportamentalFAs:
            if compFA is None:
                return False

        for compFA in self._comportamentalFAs:
            if not compFA.check():
                return False

            if len(self._comportamentalFAs) > 1:
                raise NotImplementedError

        return True
