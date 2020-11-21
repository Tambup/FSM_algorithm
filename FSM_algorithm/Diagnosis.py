import copy
from core.OutTransition import OutTransition
from LOSpaceState import LOSpaceState
from RegexOperation import RegexOperation


class Diagnosis(RegexOperation):
    final_trans = OutTransition(name='',
                                destination='FINAL',
                                links=[],
                                observable=None,
                                relevant=None)

    final_state = LOSpaceState(states=[], links=[])

    def __init__(self, space_states):
        super().__init__()
        self._space_states = space_states
        self._regex = ''

    @property
    def regex(self):
        return self._regex

    def diagnosis(self):
        self._unify_exit()
        while len(self._work_space) > 2:
            if super()._sequence_transition():
                super()._concat()
            elif super()._set_parallel_tansition():
                super()._alternative(null_evt=LOSpaceState.NULL_EVT)
            else:
                super()._remaining()

        self._regex = ''.join([
            tr.relevant if tr.relevant else LOSpaceState.NULL_EVT
            for space in self._work_space.keys()
            for tr in space.nexts.keys()])

    def _unify_exit(self):
        self._work_space = {k: None for k in copy.deepcopy(self._space_states)}
        final_st = [state for state in self._work_space.keys()
                    if state.is_final()]
        for state in final_st:
            state.add_next(Diagnosis.final_trans, Diagnosis.final_state)

        self._work_space[Diagnosis.final_state] = None
        self._prev = {}
        for state in self._work_space.keys():
            self._prev[state] = []
        for state in self._work_space.keys():
            for _, next_st in state.nexts.items():
                self._prev[next_st].append(state)

    def _new_generic_trans_given_relevance(self, relevance, nk=None):
        return OutTransition(name='',
                             destination=None,
                             links=[],
                             observable=None,
                             relevant=relevance)

    def dict_per_json(self):
        return {'regex': self._regex}
