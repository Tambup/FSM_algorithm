from .core import ComportamentalFANetwork


class Task:
    """
    This class provide a general description of a task inside FSM_algorithm.

    Should not be instantiated directly, but using the subclasses.

    :param compFAN: The ComportamentalFANetwork used in the task
    :type compFAN: :class:`~FSM_algorithm.core.ComportamentalFANetwork`
    """
    def __init__(self, compFAN):
        """
        Constructor method.
        """
        self._compFAN = compFAN

    @property
    def compFAN(self) -> ComportamentalFANetwork:
        """
        Returns the ComportamentalFANetwork used in the task.

        :return: The ComportamentalFANetwork used in the task
        :rtype: :class:`FSM_algorithm.core.ComportamentalFANetwork`
        """
        return self._compFAN

    def build(self, param=None):
        """
        A generic builder for subclasses.

        Does nothing.

        :param param: An optional parameter provided for subclasses,
            defaults to None
        :type param: list, optional
        """
        pass
