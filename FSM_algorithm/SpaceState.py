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

    @property
    def nexts(self):
        return self._nexts

    def set_link(self, link_name, link_event):
        self._links[link_name] = link_event

    def clear_link(self, link_name):
        self._links[link_name] = SpaceState.NULL_EVT

    def add_next(self, transition, next):
        self._nexts[transition] = next

    def change_state(self, old_state, new_state):
        self._nexts = {}
        self._states = [new_state if elem == old_state else elem
                        for elem in self._states]

    def is_final(self):
        for val in self._links.values():
            if val != SpaceState.NULL_EVT:
                return False

        return True

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

    def __hash__(self):
        return hash((tuple(sorted(self._links.items())), tuple(self._states)))

    def dict_per_json(self):
        temp = {}
        temp['link'] = {key: val for key, val in self._links.items()}
        temp['state'] = {
            'CFAN '+str(i): val.name for i, val in enumerate(self._states)
        }
        temp['next'] = {
            key.name: self._short_str(val) for key, val in self._nexts.items()
        }

        return temp

    def _short_str(self, next_state):
        return "state: " + str(
            [
                f"CFAN {i}: {state.name}"
                for i, state in enumerate(next_state.states)
            ]) + ", " + "link: " + str(
                [f"{name}: {val}" for name, val in next_state.links.items()]
            )
