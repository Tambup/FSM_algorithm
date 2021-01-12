import copy
from .core import OutTransition
from .LOSpaceState import LOSpaceState
from .RegexOperation import RegexOperation


class Diagnosis(RegexOperation):
    """
    This class, using :py:meth:`diagnosis()` compute the regex from a
    list of :class:`~FSM_algorithm.LOSpaceState` computed with
    :class:`~FSM_algorithm.ComportamentalFANSObservation`.

    :param space_states: The list of :class:`~FSM_algorithm.LOSpaceState`
    :type space_states: list
    :param observation: The list of observations on the
        :class:`~FSM_algorithm.core.ComportamentalFANetwork`
    :type observation: list
    """
    final_trans = OutTransition(name='',
                                destination='FINAL',
                                links=[],
                                observable=None,
                                relevant=None)

    final_state = LOSpaceState(states=[], links=[])

    def __init__(self, space_states, observation):
        """
        Constructor method.
        """
        super().__init__()
        self._space_states = space_states
        self._regex = ''
        self._observation = observation

    @property
    def regex(self):
        """
        Describe the regex computed with :py:meth:`diagnosis()`.

        :return: The computed regex
        :rtype: str
        """
        return self._regex

    def diagnosis(self):
        """
        Compute the regex relative to an observation on a
        list of :class:`~FSM_algorithm.LOSpaceState` computed with
        :class:`~FSM_algorithm.ComportamentalFANSObservation`.
        """
        print('Start computing diagnosis')
        self._unify_exit()
        while len([tr for space in self._work_space.keys()
                  for tr in space.nexts.keys()]) > 1:
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
        print('Diagnosis complete ' + self._regex)

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
        """
        Returns the object's attributes in a form easy to transform in json.

        :return: All the necessary information in a data structure
        :rtype: dict
        """
        return {
            'observation': self._observation,
            'number space states': len(self._space_states),
            'regex': self._regex
            }
