from core.OutTransition import OutTransition


class SubscriptedTransition(OutTransition):
    def __init__(self, name, destination, links,
                 observable, relevant, subscr=None):
        links = [{'link': link[0], 'type': link[1], 'event': link[2]}
                 for link in links]
        super().__init__(name, destination, links, observable, relevant)
        self._subscript_value = subscr

    @staticmethod
    def from_trans(out_trans):
        return SubscriptedTransition(name=out_trans.name,
                                     destination=out_trans.destination,
                                     links=out_trans.links,
                                     observable=out_trans.observable,
                                     relevant=out_trans.relevant)

    @property
    def subscript_value(self):
        return self._subscript_value

    def __hash__(self):
        return hash((super().__hash__(), self._subscript_value))
