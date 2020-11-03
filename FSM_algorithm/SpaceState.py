class SpaceState:
    NULL_EVT = "\u03B5"

    def __init__(self, states, links):
        self._links = {link_name: SpaceState.NULL_EVT for link_name in links}
        self._states = states
        self._nexts = {}

    def next_transition_state(self):
        possible_next = {}
        for next_state in self._states:
            trans = [out_trans for out_trans in next_state.out_transitions
                     if self._must_add(out_trans)]
            if len(trans) > 0:
                possible_next[next_state] = trans

        return possible_next

    def _must_add(self, next_out_trans):
        for link_name, link_type, link_event in next_out_trans.links:
            if link_type == "in":
                if self._links[link_name] != link_event:
                    return False
            elif link_type == "out":
                if self._links[link_name] != SpaceState.NULL_EVT:
                    return False

        return True

    @property
    def links(self):
        return self._links

    @property
    def states(self):
        return self._states

    def set_link(self, link_name, link_event):
        self._links[link_name] = link_event

    def clear_link(self, link_name):
        self._links[link_name] = SpaceState.NULL_EVT

    def add_next(self, transition, next):
        self._nexts[transition] = next

    def change_state(self, old_state, new_state):
        self._states = [new_state if elem == old_state else elem
                        for elem in self._states]

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
