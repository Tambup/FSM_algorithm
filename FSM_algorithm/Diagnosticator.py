from Closure import Closure


class Diagnosticator:
    def __init__(self, space_states):
        self._space_states = space_states
        self._closures = None

    def build(self):
        self._build_closures()

    def _build_closures(self):
        self._closures = []
        for i, state in enumerate(self._space_states):
            is_obs = False
            for trans in state.nexts.keys():
                if trans.observable:
                    is_obs = True
                    break
            if is_obs or state.is_init():
                closure = Closure(i, self._space_states)
                closure.build()
                self._closures.append(closure)
