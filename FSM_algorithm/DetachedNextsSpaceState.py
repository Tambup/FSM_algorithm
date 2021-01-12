from .SpaceState import SpaceState


class DetachedNextsSpaceState(SpaceState):
    """
    This class represent a Space State of the state
    :class:`~FSM_algorithm.ComportamentalFANSpace.ComportamentalFANSpace`.

    This can be seen as a vertex of a oriented graph, where the graph is
    represented by
    :class:`~FSM_algorithm.ComportamentalFANSpace.ComportamentalFANSpace`.

    :param space_state: The Space State from from which is derived
    :type space_state: :class:`~FSM_algorithm.SpaceState.SpaceState`
    :param is_closure_init: If, inside a closure, this is the init state
    :type is_closure_init: bool, optional
    """
    def __init__(self, space_state, is_closure_init=False):
        """
        Constructor method.
        """
        super().__init__(links=[], states=space_state.states)
        self._links = space_state.links
        self._id = space_state.id
        self._nexts = space_state.nexts
        self._external_nexts = {}
        self._is_closure_init = is_closure_init

    @property
    def external_nexts(self):
        """
        Contains the list of all the pair transition-successor
        that exit the :class:`~FSM_algorithm.Closure` which the current
        DetachedNextsSpaceState belongs to.

        :return: All the pair transition-successor exiting the current Closure
        :rtype: dict
        """
        return self._external_nexts

    @property
    def nexts(self):
        return self._nexts

    @nexts.setter
    def nexts(self, value):
        self._nexts = {}
        for k, v in value.items():
            if k.observable:
                self._external_nexts[k] = v
            else:
                self._nexts[k] = v

    def is_closure_init(self):
        return self._is_closure_init

    def to_decorate(self):
        """
        Declare if the current DetachedNextsSpaceState must
        to be decorated or not.

        :return: True if the current DetachedNextsSpaceState must
            be decorated, else False
        :rtype: bool
        """
        if super().is_final():
            return True
        if self._external_nexts:
            return True
        return False

    def exit_state(self):
        """
        Declare if the current DetachedNextsSpaceState has transitions
        exiting the current :class:`~FSM_algorithm.Closure`.

        :return: True if the current DetachedNextsSpaceState has transitions
            exiting the current :class:`~FSM_algorithm.Closure`, else False
        :rtype: bool
        """
        return True if self._external_nexts else False
