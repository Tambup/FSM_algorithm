from core.OutTransition import OutTransition


class SubscriptedTransition(OutTransition):
    def __init__(self, name, destination, links, observable, relevant, subscr):
        super().__init__(name, destination, links, observable, relevant)
        self._subscript_value = subscr

    @property
    def subscript_value(self):
        return self._subscript_value
