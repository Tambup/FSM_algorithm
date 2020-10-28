from core.OutTransition import OutTransition


class State():
    def __init__(self, name, isInit, outTransitions):
        self.name = name
        self.isInit = isInit
        self.outTransitions = []
        for outTransition in outTransitions:
            self.outTransitions.append(
                OutTransition(name=outTransition["name"],
                              destination=outTransition["destination"],
                              links=outTransition["link"],
                              observable=outTransition["observable"],
                              relevant=outTransition["relevant"])
            )
