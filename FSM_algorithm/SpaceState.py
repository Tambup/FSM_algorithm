class SpaceState:
    """
    This class represent a Space State of the state
    :class:`~FSM_algorithm.ComportamentalFANSpace.ComportamentalFANSpace`.

    This can be seen as a vertex of a oriented graph, where the graph is
    represented by
    :class:`~FSM_algorithm.ComportamentalFANSpace.ComportamentalFANSpace`.

    :param states: the list of :class:`~FSM_algorithm.core.State.State` that
        constitute the Space State.
    :type states: list
    :param links: the list of
        :class:`~FSM_algorithm.core.OutTransition.OutTransition` in
        the Space State.
    :type links: list
    """
    NULL_EVT = '\u03B5'

    def __init__(self, states, links):
        """
        Constructor method.
        """
        self._links = {link_name: SpaceState.NULL_EVT for link_name in links}
        self._states = states
        self._nexts = {}
        self._id = None

    def next_transition_state(self):
        """
        Returns all the possible successor States
        (:class:`~FSM_algorithm.core.State`) of the current SpaceState.

        :return: A dict where the key is a :class:`~FSM_algorithm.core.State`
            and the value a list of tuples containing index and transition
        :rtype: dict
        """
        possible_next = {}
        for i, next_state in enumerate(self._states):
            trans = [out_trans for out_trans in next_state.out_transitions
                     if self._must_add(out_trans)]
            if trans:
                possible_next[next_state] = (i, trans)
        print('added ' + str(len(possible_next)) + ' transition.\n')
        return possible_next

    def _must_add(self, next_out_trans):
        for link_name, link_type, link_event in next_out_trans.links:
            if link_type == 'in':
                if self._links[link_name] != link_event:
                    return False
            elif link_type == 'out':
                if self._links[link_name] != SpaceState.NULL_EVT:
                    return False

        return True

    @property
    def id(self):
        """
        Describe the id of the current SpaceState.

        :return: Returns the id of the current SpaceState
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def links(self):
        """
        Returns all the links, with their value, of the current SpaceState.

        :return: Sll the links, with their value, of the current SpaceState
        :rtype: dict
        """
        return self._links

    @property
    def states(self):
        """
        Returns all the :class:`~FSM_algorithm.core.State` of the
        current SpaceState.

        :return: All the links, with their value, of the current SpaceState
        :rtype: dict
        """
        return self._states

    @property
    def nexts(self):
        """
        Returns all the successor, until this point of the search,
        of the current SpaceState.

        :return: All the successor, until this point of the search,
            of the current SpaceState.
        :rtype: dict
        """
        return self._nexts

    @nexts.setter
    def nexts(self, value):
        self._nexts = value

    def set_link(self, link_name, link_event):
        """
        Set the value of a particular link.

        :param link_name: The name of the link
        :type link_name: str
        :param link_event: The value the link will assume
        :type link_event: str
        """
        self._links[link_name] = link_event

    def clear_link(self, link_name):
        """
        Calling this will clear the value of the link.
        Clear means set the value to the NULL event.

        :param link_name: The name of the link
        :type link_name: str
        """
        self._links[link_name] = SpaceState.NULL_EVT

    def add_next(self, transition, next):
        """
        Add a new successor to the current SpaceState.

        :param transition: The transition used to go to the successor
        :type transition: :class:`~FSM_algorithm.core.OutTransition`
        :param next: The new successor SpaceState
        :type next: :class:`~FSM_algorithm.SpaceState`
        """
        self._nexts[transition] = next

    def update_nexts(self, del_tr, new_tr, new_next):
        """
        The transition associated with a successor is substituted with another
        to another successor.

        :param del_tr: The transition that must be removed
        :type del_tr: :class:`~FSM_algorithm.core.OutTransition`
        :param new_tr: The new transition
        :type new_tr: :class:`~FSM_algorithm.core.OutTransition`
        :param new_next: The new successor
        :type new_next: :class:`~FSM_algorithm.SpaceState`
        """
        for to_del in del_tr:
            del self._nexts[to_del]
        self._nexts[new_tr] = new_next

    def change_state(self, old_state, new_state):
        """
        Change one of the :class:`~FSM_algorithm.core.State` that
        form the SpaceState

        :param old_state: The State to be eliminated
        :type old_state: `FSM_algorithm.core.State`
        :param new_state: The State to be inserted
        :type new_state: `FSM_algorithm.core.State`
        """
        self._nexts = {}
        self._states = [new_state if elem == old_state else elem
                        for elem in self._states]

    def is_final(self):
        """
        Check if the current SpaceState is final or not.

        :return: True if the current SpaceState is final, else False
        :rtype: bool
        """
        for val in self._links.values():
            if val != SpaceState.NULL_EVT:
                return False

        return True

    def is_init(self):
        """
        Check if the current SpaceState is initial or not.

        :return: True if the current SpaceState is initial, else False
        :rtype: bool
        """
        for state in self._states:
            if not state.is_init():
                return False
        for link in self._links.values():
            if link != SpaceState.NULL_EVT:
                return False

        return True

    def is_closure_init(self):
        """
        Check if the current SpaceState is initial for a
        :class:`~FSM_algorithm.Closure` or not.

        :return: True if the current SpaceState is initial
            for a :class:`~FSM_algorithm.Closure`, else False
        :rtype: bool
        """
        return self.is_init()

    def __eq__(self, obj):
        if isinstance(obj, SpaceState):
            if len(self._states) != len(obj.states):
                return False

            for i, val in enumerate(self._states):
                if val != obj.states[i]:
                    return False

            if len(self._links) != len(obj.links):
                return False

            for name, value in self._links.items():
                if value != obj.links[name]:
                    return False

            for name, value in obj.links.items():
                if self._links[name] != value:
                    return False

            return True

    def __hash__(self):
        return hash((tuple(sorted(self._links.items())), tuple(self._states)))

    def auto_trans(self):
        """
        Check if the current SpaceState has an autotransition or not.

        :return: True if there is an autotransition, else False
        :rtype: bool
        """
        for trns, succ in self._nexts.items():
            if succ == self:
                return trns

    def dict_per_json(self):
        """
        Returns the object's attributes in a form easy to transform in json.

        :return: All the necessary information in a data structure
        :rtype: dict
        """
        temp = {}
        temp['name'] = self._id
        temp['link'] = {key: val for key, val in self._links.items()}
        temp['state'] = {
            'CFAN '+str(i): val.name for i, val in enumerate(self._states)
        }
        temp['next'] = {
            k.name: self._next_desc(val, k) for k, val in self._nexts.items()
        }

        return temp

    def _next_desc(self, next_state, out_trans):
        temp = {}
        temp['state'] = {
            f'CFAN {i}': st.name for i, st in enumerate(next_state.states)
        }
        temp['link'] = {name: val for name, val in next_state.links.items()}
        temp['observable'] = out_trans.observable
        temp['relevant'] = out_trans.relevant

        return temp
