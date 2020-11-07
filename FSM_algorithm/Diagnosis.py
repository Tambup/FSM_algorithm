import copy
from core.OutTransition import OutTransition


class Diagnosis:
    final_trans = OutTransition(name='',
                                destination='FINAL',
                                links=[],
                                observable=[],
                                relevant=[])

    def __init__(self, space_states):
        self._space_states = copy.copy(space_states)

    def diagnosis(self):
        self._unify_exit()

    def _unify_exit(self):
        final_st = [state for state in self._space_states if state.is_final()]

        for space_state in final_st:
            space_state.add_next(Diagnosis.final_trans, 'FINAL')
