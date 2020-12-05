from SpaceState import SpaceState


class DetachedNextsSpaceState(SpaceState):
    def __init__(self, space_state, is_closure_init=False):
        super().__init__(links=[], states=space_state.states)
        self._links = space_state.links
        self._id = space_state.id
        self._nexts = space_state.nexts
        self._external_nexts = {}
        self._is_closure_init = is_closure_init

    @property
    def external_nexts(self):
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
        if super().is_final():
            return True
        if self._external_nexts:
            return True
        return False

    def exit_state(self):
        return True if self._external_nexts else False
