class SpaceState:
    NULL_EVT = '\u03B5'

    def __init__(self, states, links):
        self._links = {link_name: SpaceState.NULL_EVT for link_name in links}
        self._states = states
        self._nexts = {}
        self._id = None

    def next_transition_state(self):
        possible_next = {}
        for i, next_state in enumerate(self._states):
            trans = [out_trans for out_trans in next_state.out_transitions
                     if self._must_add(out_trans)]
            if trans:
                possible_next[next_state] = (i, trans)

        return possible_next

    def _must_add(self, next_out_trans):
        for link_name, link_type, link_event in next_out_trans.links:
            if link_type == 'in':
                if self._links[link_name] != link_event:
                    return False
            elif link_type == 'out':
                if self._links[link_name] != SpaceState.NULL_EVT:
                    return False

        return True

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def links(self):
        return self._links

    @property
    def states(self):
        return self._states

    @property
    def nexts(self):
        return self._nexts

    @nexts.setter
    def nexts(self, value):
        self._nexts = value

    def set_link(self, link_name, link_event):
        self._links[link_name] = link_event

    def clear_link(self, link_name):
        self._links[link_name] = SpaceState.NULL_EVT

    def add_next(self, transition, next):
        self._nexts[transition] = next

    def update_nexts(self, del_tr, new_tr, new_next):
        for to_del in del_tr:
            del self._nexts[to_del]
        self._nexts[new_tr] = new_next

    def change_state(self, old_state, new_state):
        self._nexts = {}
        self._states = [new_state if elem == old_state else elem
                        for elem in self._states]

    def is_final(self):
        for val in self._links.values():
            if val != SpaceState.NULL_EVT:
                return False

        return True

    def is_init(self):
        for state in self._states:
            if not state.is_init():
                return False
        for link in self._links.values():
            if link != SpaceState.NULL_EVT:
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

    def auto_trans(self):
        for trns, succ in self._nexts.items():
            if succ == self:
                return trns

    def dict_per_json(self):
        temp = {}
        temp['name'] = self._id
        temp['link'] = {key: val for key, val in self._links.items()}
        temp['state'] = {
            'CFAN '+str(i): val.name for i, val in enumerate(self._states)
        }
        temp['next'] = {
            k.name: self._next_desc(val, k) for k, val in self._nexts.items()
        }

        return temp

    def _next_desc(self, next_state, out_trans):
        temp = {}
        temp['state'] = {
            f'CFAN {i}': st.name for i, st in enumerate(next_state.states)
        }
        temp['link'] = {name: val for name, val in next_state.links.items()}
        temp['observable'] = out_trans.observable
        temp['relevant'] = out_trans.relevant

        return temp
