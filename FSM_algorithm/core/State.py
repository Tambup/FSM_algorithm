from .OutTransition import OutTransition


class State:
    """
    This class represent a state in a
    :class:`~FSM_algorithm.core.ComportamentalFA`.

    :param name: Name of the state
    :type name: str
    :param is_init: Describe if the current state is initial or not
    :type is_init: bool
    :param out_transitions: The list of transitions exiting
        from the current state
    :type out_transitions: list
    """
    def __init__(self, name, is_init, out_transitions):
        """
        Constructor method.
        """
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
        """
        Describe the name of the current state.

        :return: Returns the name of the current state
        :rtype: str
        """
        return self._name

    @property
    def out_transitions(self):
        """
        These are the transitions exiting the current state

        :return: Returns the list of transitions exiting of the current state
        :rtype: list
        """
        return self._out_transitions

    def in_links(self):
        """
        Returns the list of links entering in the state

        :return: The list of links entering in the state
        :rtype: list
        """
        return {link for out_trans in self._out_transitions
                for link in out_trans.in_links()}

    def out_links(self):
        """
        Returns the list of links exiting in the state

        :return: The list of links exiting in the state
        :rtype: list
        """
        return {link for out_trans in self._out_transitions
                for link in out_trans.out_links()}

    def __eq__(self, obj):
        if isinstance(obj, State):
            temp = self._name == obj.name and self._is_init == obj.is_init()
            if self._out_transitions is None or obj.out_transitions is None:
                return False if self._out_transitions is not None \
                    or obj.out_transitions is not None else temp

            if temp and len(self._out_transitions) == len(obj.out_transitions):
                if not set(self._out_transitions).issubset(
                            obj.out_transitions):
                    return False

                if not set(obj.out_transitions).issubset(
                            self._out_transitions):
                    return False

                return True
        return False

    def __hash__(self):
        return hash((self._name, self._is_init, tuple(self._out_transitions)))

    def check(self):
        """
        Check if the state is correct.

        Correct means that the state has a name, all transitions have names,
        are correct and different each other.


        :return: True if the state is correct, else false
        :rtype: bool
        """
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
        """
        Check if the current state has at least one transition
        exiting the state.

        In this case an autotransition is not considered an exiting state.

        :return: True if there is a transition going to another state,
            else False
        :rtype: bool
        """
        if self._out_transitions is None:
            return True

        for out_trans in self._out_transitions:
            if out_trans.destination != self._name:
                return False

        return True

    def is_init(self):
        """
        Check if the current state is an inital state or not

        :return: True if the current state is initial, else False
        :rtype: bool
        """
        return self._is_init
