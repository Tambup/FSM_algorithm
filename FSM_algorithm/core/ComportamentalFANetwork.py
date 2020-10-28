from core.ComportamentalFA import ComportamentalFA


class ComportamentalFANetwork():
    def __init__(self, name, CFAs):
        self.name = name
        self.comportamentalFAs = []
        for cfa in CFAs:
            self.comportamentalFAs.append(ComportamentalFA(name=cfa["name"],
                                          states=cfa["state"]))
