from Closure import Closure


class Diagnosticator:
    def __init__(self, space_states):
        self._space_states = space_states
        self._closures = None

    def build(self):
        self._build_closures()

    def _build_closures(self):
        closable = {}
        for act in self._space_states:
            if act.is_init():
                closable[act] = None
            for trans, state in act.nexts.items():
                if trans.observable:
                    closable[state] = None
        closable = [self._space_states.index(elem) for elem in closable.keys()]
        self._closures = []
        for index in closable:
            closure = Closure(enter_state_index=index,
                              state_space=self._space_states)
            closure.build()
            self._closures.append(closure)
