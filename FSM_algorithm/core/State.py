from core.OutTransition import OutTransition


class State():
    def __init__(self, name, is_init, out_transitions):
        self._name = name
        self._is_init = is_init
        self._out_transitions = []
        for out_transition in out_transitions:
            self._out_transitions.append(
                OutTransition(name=out_transition['name'],
                              destination=out_transition['destination'],
                              links=out_transition['link'],
                              observable=out_transition['observable'],
                              relevant=out_transition['relevant'])
            )

    @property
    def name(self):
        return self._name

    @property
    def out_transitions(self):
        return self._out_transitions

    def in_links(self):
        return {link for out_trans in self._out_transitions
                for link in out_trans.in_links()}

    def out_links(self):
        return {link for out_trans in self._out_transitions
                for link in out_trans.out_links()}

    def __eq__(self, obj):
        raise NotImplementedError

    def check(self):
        if self._name is None:
            return False

        for out_trans in self._out_transitions:
            if out_trans.name is None:
                return False
            elif not out_trans.check():
                return False

        for out_trans in self._out_transitions:
            for in_trans in self._out_transitions:
                if out_trans is not in_trans:
                    if out_trans == in_trans:
                        return False

        return True

    def no_exit(self):
        if self._out_transitions is None:
            return True

        for out_trans in self._out_transitions:
            if out_trans.destination != self._name:
                return False

        return True

    def is_init(self):
        return self._is_init
