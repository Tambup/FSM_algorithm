from .SpaceState import SpaceState


class LOSpaceState(SpaceState):
    """
    This class represent a Space State of the state
    :class:`~FSM_algorithm.ComportamentalFANSObservation.ComportamentalFANSObservation`.

    This can be seen as a vertex of a oriented graph, where the graph is
    represented by
    :class:`~FSM_algorithm.ComportamentalFANSObservation.ComportamentalFANSObservation`.
    Every LOSpaceState has additional information regarding observation of the
    state such as :py:attr:`obs_index`.

    :param states: the list of :class:`~FSM_algorithm.core.State.State` that
        constitute the Space State.
    :type states: list
    :param links: the list of
        :class:`~FSM_algorithm.core.OutTransition.OutTransition` in
        the Space State.
    :type links: list
    """
    def __init__(self, states, links):
        """
        Constructor method.
        """
        super().__init__(states, links)
        self._obs_index = None
        self._has_next_obs = True

    @property
    def obs_index(self):
        """
        Describe the index of the observation
        given a observation list.

        By example the initial state has obs_index 0, and the first
        successor reach by a transition with an allowed observation
        has obs_index 1.

        :return: The index of the observation read until this LOSpaceState
        :rtype: int
        """
        return self._obs_index

    @obs_index.setter
    def obs_index(self, value):
        self._obs_index = value

    def set_has_obs(self, val):
        """
        Set the information about the presence of remaining elements in
        the observation.

        This is necessary to understand if the current LOSpaceState is final
        or not in :py:meth:`is_final()`

        :param val: True if there are remaining elements in
            the observation, else False
        :type val: bool
        """
        self._has_next_obs = val

    def next_transition_state(self, obs_val):
        """
        Returns all the possible successor States
        (:class:`~FSM_algorithm.core.State`) of the current LOSpaceState
        relative to a particular observation.

        This means that the transition must be null or equal to obs_val.

        :param obs_val: The observation to be used for the search
        :type obs_val: str
        :return: A dict where the key is a :class:`~FSM_algorithm.core.State`
            and the value a list of tuples containing index and transition
        :rtype: dict
        """
        possible_next = {}
        for i, next_state in enumerate(self._states):
            trans = [out_trans for out_trans in next_state.out_transitions
                     if self._must_add(out_trans, obs_val)]
            if trans:
                possible_next[next_state] = (i, trans)
                print('added ' + str(len(trans)) + ' transition.\n')
        return possible_next

    def _must_add(self, next_out_trans, obs_val):
        obs_list = next_out_trans.observable
        if not obs_list or obs_val == obs_list:
            return super()._must_add(next_out_trans)

        return False

    def is_final(self):
        """
        Check if the current LOSpaceState is final or not

        :return: True if the current LOSpaceState is final, else False
        :rtype: bool
        """
        if self._has_next_obs:
            return False
        return super().is_final()

    def __hash__(self):
        return hash((super().__hash__(), self._obs_index))

    def __eq__(self, obj):
        if isinstance(obj, LOSpaceState):
            if super().__eq__(obj):
                return obj.obs_index == self._obs_index

        return False

    def dict_per_json(self):
        temp = {}
        temp['name'] = self._id
        temp['obs_index'] = self._obs_index
        temp['link'] = {key: val for key, val in self._links.items()}
        temp['state'] = {
            'CFAN '+str(i): val.name for i, val in enumerate(self._states)
        }
        temp['next'] = {
            k.name: self._short_next_desc(val, k)
            for k, val in self._nexts.items()
        }

        return temp

    def _short_next_desc(self, next_state, out_trans):
        temp = {}
        temp['state'] = {
            f'CFAN {i}': st.name for i, st in enumerate(next_state.states)
        }
        temp['link'] = {name: val for name, val in next_state.links.items()}

        return temp
