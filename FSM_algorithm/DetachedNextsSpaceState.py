from SpaceState import SpaceState


class DetachedNextsSpaceState(SpaceState):
    def __init__(self, space_state):
        super().__init__(links=[], states=space_state.states)
        self._links = space_state.links
        self._id = space_state.id
        self._nexts = space_state.nexts
        self._external_nexts = {}

    @property
    def external_nexts(self):
        return self._external_nexts

    @property
    def nexts(self):
        return self._nexts

    @nexts.setter
    def nexts(self, value):
        for k, v in value.items():
            if k.observable:
                del self._nexts[k]
                self._external_nexts[k] = v

    def is_final(self):
        if super().is_final():
            return True
        if self._external_nexts:
            return True
        return False
