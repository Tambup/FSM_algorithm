from .OutTransition import OutTransition


class SubscriptedTransition(OutTransition):
    """
    This class is a transition that has a subscription value, useful when
    a :class:`~FSM_algorithm.Closure` has to annotate a subscription during
    the regex computation.

    :param name: Name of the transition
    :type name: str
    :param destination: Name/number/id of the destination state
    :type destination: str
    :param links: The list of links associated with the transition
    :type links: list
    :param observable: The observation associated with the transition
    :type observable: str
    :param relevant: The relevance associated with the transition
    :type relevant: str
    :param subscr: The subscription value, defaults to None
    :type subscr: int, optional
    """

    def __init__(self, name, destination, links,
                 observable, relevant, subscr=None):
        """
        Constructor method.
        """
        links = [{'link': link[0], 'type': link[1], 'event': link[2]}
                 for link in links]
        super().__init__(name, destination, links, observable, relevant)
        self._subscript_value = subscr

    @staticmethod
    def from_trans(out_trans):
        """
        Build a :class:`~FSM_algorithm.core.SubscriptedTransition` from a
        :class:`~FSM_algorithm.core.OutTransition`.

        :param out_trans: The starting
            :class:`~FSM_algorithm.core.OutTransition`
        :type out_trans: :class:`~FSM_algorithm.core.OutTransition`
        :return: Returns a
            :class:`~FSM_algorithm.core.SubscriptedTransition` derived
            from a :class:`~FSM_algorithm.core.OutTransition`
        :rtype: :class:`~FSM_algorithm.core.SubscriptedTransition`
        """
        return SubscriptedTransition(name=out_trans.name,
                                     destination=out_trans.destination,
                                     links=out_trans.links,
                                     observable=out_trans.observable,
                                     relevant=out_trans.relevant)

    @property
    def subscript_value(self):
        """
        This attribute is used to distinguish, during the regex computation,
        transition belonging to different final states.

        :return: The subscription value of the transition
        :rtype: int
        """
        return self._subscript_value

    def __hash__(self):
        return hash((super().__hash__(), self._subscript_value))
