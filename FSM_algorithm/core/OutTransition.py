class OutTransition():
    """
    This class represent an out transition from a
    :class:`~FSM_algorithm.core.State` to another of a
    :class:`~FSM_algorithm.core.ComportamentalFA`.

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
    """
    nonce = 0

    def __init__(self, name, destination, links, observable, relevant):
        """
        Constructor method.
        """
        self._name = name
        self._destination = destination
        self._links = frozenset(
            (link['link'], link['type'], link['event']) for link in links
            )
        self._observable = observable
        self._relevant = relevant
        self._nonce = OutTransition.nonce
        OutTransition.nonce += 1

    @property
    def name(self):
        """
        Describe the name associated with the transition.

        :return: Returns the name associated with the transition
        :rtype: str
        """
        return self._name

    @property
    def destination(self):
        """
        Describe the destination associated with the transition.

        :return: Returns the destination associated with the transition
        :rtype: str
        """
        return self._destination

    @property
    def observable(self):
        """
        Describe the observation associated with the transition.

        :return: Returns the observation associated with the transition
        :rtype: str
        """
        return self._observable

    @property
    def relevant(self):
        """
        Describe the relevance associated with the transition.

        :return: Returns the relevance associated with the transition
        :rtype: str
        """
        return self._relevant

    @property
    def links(self):
        """
        This is the list of links associated with the transition.

        :return: Returns the list of links associated with the transition
        :rtype: list
        """
        return self._links

    def in_links(self):
        """
        Returns the list of links entering in the transition

        :return: The list of links entering in the transition
        :rtype: list
        """
        return [link[0] for link in self._links if link[1] == 'in']

    def out_links(self):
        """
        Returns the list of links exiting in the transition

        :return: The list of links exiting in the transition
        :rtype: list
        """
        return [link[0] for link in self._links if link[1] == 'out']

    def check(self):
        """
        Check if the transition is correct.

        Correct means that the transition has a destination, all links are
        meaningfull, there is no more than one entering link and every
        exiting link has a unique name.

        :return: True if the Transition is correct, else false
        :rtype: bool
        """
        if self._destination is None:
            return False

        for link in self._links:
            if link[0] is None or link[1] is None or link[1] is None:
                return False

        in_link_exist = False
        for _, link_type, _ in self._links:
            if link_type == 'in':
                if in_link_exist:
                    return False
                in_link_exist = True

        for link in self._links:
            for inner_link in self._links:
                if link is not inner_link:
                    if link[1] == 'out' and inner_link[1] == 'out':
                        if link[0] == inner_link[0]:
                            return False
        return True

    def __eq__(self, obj):
        if isinstance(obj, OutTransition):
            if self._name == obj.name and \
                    self._destination == obj.destination and \
                    self._observable == obj.observable and \
                    self._relevant == obj.relevant:
                if self._links is not None and obj.links is not None:
                    if self._same_vectors(obj):
                        return True
        return False

    def __hash__(self):
        return hash((self._name, self._destination, self._links, self._nonce))

    def _same_vectors(self, obj):
        return all(elem in self._links for elem in obj.links) and \
                all(elem in obj.links for elem in self._links)

    def sameEvents(self, oth_links):
        """
        Check if the current transition has the same links of the
        one passed in.

        :param oth_links: A list of tuples representing links
            of another transition
        :type oth_links: list
        :return: True if are equals, else False
        :rtype: bool
        """
        both_null = False
        if self._links is None or oth_links is None:
            if self._links is not None or oth_links is not None:
                return False
            else:
                both_null = True

        if not both_null:
            for link in self._links:
                is_contained = False
                for oth_link in oth_links:
                    if link[2] == oth_link[2]:
                        if link[1] == oth_link[1]:
                            is_contained = True
                            break
                if not is_contained:
                    return False

            for oth_link in oth_links:
                is_contained = False
                for link in self._links:
                    if link[2] == oth_link[2]:
                        if link[1] == oth_link[1]:
                            is_contained = True
                            break
                if not is_contained:
                    return False
            return True

        return False
