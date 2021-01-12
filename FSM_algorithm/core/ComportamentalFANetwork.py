from .ComportamentalFA import ComportamentalFA


class ComportamentalFANetwork:
    """
    This class represent a Comportamental Finite Automa Network
    (ComportamentalFAN).

    :param name: The name of the ComportamentalFA
    :type name: str
    :param CFAs: The list of ComportamentalFA of the ComportamentalFAN
    :type CFAs: list
    """
    def __init__(self, name, CFAs):
        """
        Constructor method.
        """
        self._name = name
        self._comportamentalFAs = []
        for cfa in CFAs:
            self._comportamentalFAs.append(ComportamentalFA(name=cfa["name"],
                                           states=cfa["state"]))

    @property
    def name(self):
        """
        Describe the name of the current ComportamentalFAN.

        :return: Returns the name of the current ComportamentalFAN
        :rtype: str
        """
        return self._name

    @property
    def comportamentalFAs(self):
        """
        These are the ComportamentalFA that are members
        of the current ComportamentalFAN.

        :return: Returns the list of the ComportamentalFA
            of the current ComportamentalFAN
        :rtype: list
        """
        return self._comportamentalFAs

    def in_links(self):
        """
        Returns the list of links entering in the ComportamentalFAN

        :return: The list of links entering in the ComportamentalFAN
        :rtype: list
        """
        return {link for compFa in self._comportamentalFAs
                for link in compFa.in_links()}

    def out_links(self):
        """
        Returns the list of links exiting in the ComportamentalFAN

        :return: The list of links exiting in the ComportamentalFAN
        :rtype: list
        """
        return {link for compFa in self._comportamentalFAs
                for link in compFa.out_links()}

    def check(self):
        """
        Check if the ComportamentalFAN is correct.

        orrect means that the ComportamentalFAN has at least one
        :class:`~FSM_algorithm.core.ComportamentalFA`, that all the
        ComportamentalFA are correct, and all links between the
        differents ComportamentalFA are well formed.

        :return: True if the state is correct, else false
        :rtype: bool
        """
        if self._comportamentalFAs is None:
            return False

        if len(self._comportamentalFAs) < 1:
            return False

        for compFA in self._comportamentalFAs:
            if compFA is None:
                return False

        for compFA in self._comportamentalFAs:
            if not compFA.check():
                return False

        if len(self._comportamentalFAs) > 1:
            for compFA in self._comportamentalFAs:
                for in_link in compFA.in_links():
                    num_out = 0
                    for inner_compFA in self._comportamentalFAs:
                        if compFA is not inner_compFA:
                            inner_in_links = inner_compFA.in_links()
                            if set([in_link]).issubset(inner_in_links):
                                return False

                            for inner_out_link in inner_compFA.out_links():
                                if in_link == inner_out_link:
                                    num_out += 1
                                if num_out > 1:
                                    return False

                    if num_out != 1:
                        return False

                for out_link in compFA.out_links():
                    num_in = 0
                    for inner_compFA in self._comportamentalFAs:
                        if compFA is not inner_compFA:
                            inner_out_links = inner_compFA.out_links()
                            if set([out_link]).issubset(inner_out_links):
                                return False

                            for inner_in_link in inner_compFA.in_links():
                                if out_link == inner_in_link:
                                    num_in += 1
                                if num_in > 1:
                                    return False

                    if num_in != 1:
                        return False

        return True
