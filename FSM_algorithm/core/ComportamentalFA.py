from .State import State


class ComportamentalFA:
    """
    This class represent a Comportamental Finite Automa (ComportamentalFA).

    :param name: The name of the ComportamentalFA
    :type name: str
    :param states: The list of states of the ComportamentalFA
    :type states: list
    """
    def __init__(self, name, states):
        """
        Constructor method.
        """
        self._name = name
        self._states = []
        for state in states:
            self._states.append(State(name=state["name"],
                                is_init=state["init"],
                                out_transitions=state["outTransition"])
                                )

    @property
    def name(self):
        """
        Describe the name of the current ComportamentalFA.

        :return: Returns the name of the current ComportamentalFA
        :rtype: str
        """
        return self._name

    @property
    def states(self):
        """
        These are the states that are members of the current ComportamentalFA.

        :return: Returns the list of the states of the current ComportamentalFA
        :rtype: list
        """
        return self._states

    def in_links(self):
        """
        Returns the list of links entering in the ComportamentalFA

        :return: The list of links entering in the ComportamentalFA
        :rtype: list
        """
        return {link for state in self._states
                for link in state.in_links()}

    def out_links(self):
        """
        Returns the list of links exiting in the ComportamentalFA

        :return: The list of links exiting in the ComportamentalFA
        :rtype: list
        """
        return {link for state in self._states
                for link in state.out_links()}

    def __eq__(self, obj):
        if isinstance(obj, ComportamentalFA):
            temp = self._name == obj.name
            if self._states is None or obj.states is None:
                return False if self._states is not None \
                    or obj.states is not None else temp

            if temp and len(self._states) == len(obj.states):
                if not set(self._states).issubset(obj.states):
                    return False

                if not set(obj.states).issubset(self._states):
                    return False

                return True
        return False

    def _no_enter(self, state):
        for inner_state in self._states:
            if state is not inner_state:
                if inner_state.out_transitions is not None:
                    for out_trans in inner_state.out_transitions:
                        if out_trans.destination == state.name:
                            return False

        return True

    def init_state(self):
        """
        Returns the initial state of the current ComportamentalFA

        :return: The initial state of the current ComportamentalFA
        :rtype: :class:`~FSM_algorithm.core.State`
        """
        for state in self._states:
            if state.is_init():
                return state

    def check(self):
        """
        Check if the ComportamentalFA is correct.

        Correct means that the ComportamentalFA has at least one
        :class:`~FSM_algorithm.core.State`, that all the states are correct,
        with different names and every transition has a legal destination.


        :return: True if the state is correct, else false
        :rtype: bool
        """
        if self._states is None:
            return False
        if len(self._states) < 1:
            return False

        for state in self._states:
            if state is None:
                return False
            elif not state.check():
                return False

        init_counter = 0
        for state in self._states:
            if len(self._states) > 1:
                if state.no_exit() and self._no_enter(state):
                    return False

            init_counter = init_counter+1 if state.is_init() else init_counter
            for inner_state in self._states:
                if state is not inner_state:
                    if state.name is None or inner_state.name is None:
                        return False
                    elif state.name == inner_state.name:
                        return False

            for out_trans in state.out_transitions:
                must_continue = False
                for inner_state in self._states:
                    if out_trans.destination == inner_state.name:
                        must_continue = True
                        break

                if not must_continue:
                    return False

        return init_counter == 1
