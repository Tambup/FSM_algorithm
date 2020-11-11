import copy
from core.OutTransition import OutTransition


class Diagnosis:
    final_trans = OutTransition(name='',
                                destination='FINAL',
                                links=[],
                                observable=None,
                                relevant=None)

    def __init__(self, space_states):
        self._space_states = copy.copy(space_states)
        self._regex = ''

    @property
    def regex(self):
        return self._regex

    def diagnosis(self):
        self._unify_exit()
        while not self._space_states:
            if self._exist_sequence_transition():
                pass
            elif self._exist_set_parallel_tansition():
                pass
            else:
                pass

        return self._regex

    def _unify_exit(self):
        final_st = [state for state in self._space_states if state.is_final()]

        for space_state in final_st:
            space_state.add_next(Diagnosis.final_trans, 'FINAL')

    def _exist_sequence_transition(self):
        pass

    def _exist_set_parallel_tansition(self):
        pass
