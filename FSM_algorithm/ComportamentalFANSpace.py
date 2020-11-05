import copy
from Task import Task
from SpaceState import SpaceState


class ComportamentalFANSpace(Task):
    def __init__(self, compFAN):
        super().__init__(compFAN)
        self._space_states = []

    def build(self, param=None):
        self._initialize()

        index = 0
        id = 1
        while (index < len(self._space_states)):
            actual_space_state = self._space_states[index]
            next_trans_state = actual_space_state.next_transition_state()
            id = self._add_states(actual_space_state, next_trans_state, id)
            index += 1

        self._prune()

    def _init_instance(self, init_states, link_names):
        return [SpaceState(init_states, link_names)]

    def _initialize(self) -> SpaceState:
        compFAs = super().compFAN.comportamentalFAs
        link_names = super().compFAN.in_links()
        init_states = [compFA.init_state() for compFA in compFAs]
        self._space_states = self._init_instance(init_states, link_names)
        self._space_states[0].id = 0

    def _add_states(self, space_state, next_transition, id):
        num_comp_FA = 0
        for actual_state in space_state.states:
            try:
                actual_out_trans_list = next_transition[actual_state]
                for actual_out_trans in actual_out_trans_list:
                    for candidate in super().compFAN \
                            .comportamentalFAs[num_comp_FA].states:
                        if actual_out_trans.destination == candidate.name:
                            break

                    new_spc_st = self._new_state(space_state, actual_state,
                                                 candidate, actual_out_trans)
                    try:
                        index = self._space_states.index(new_spc_st)
                        space_state.add_next(actual_out_trans,
                                             self._space_states[index])
                    except ValueError:
                        new_spc_st.id = id
                        id += 1
                        self._space_states.append(new_spc_st)
                        space_state.add_next(actual_out_trans, new_spc_st)
            except KeyError:
                pass
            num_comp_FA += 1
        return id

    def _new_state(self, old_space, old_state, new_state, out_trans):
        new_space = copy.deepcopy(old_space)
        for link_name, link_type, link_event in out_trans.links:
            if link_type == "out":
                new_space.set_link(link_name, link_event)
            else:
                new_space.clear_link(link_name)

        new_space.change_state(old_state, new_state)
        return new_space

    def _prune(self):
        mantain_list = {}
        remove_list = {}
        for state in self._space_states:
            try:
                mantain_list[state] & remove_list[state]
            except KeyError:
                self._prune_recursion(state, {}, mantain_list, remove_list)

        self._space_states = list(mantain_list.keys())

    def _prune_recursion(self, state, forbidden, mantain_list, remove_list):
        if state.is_final():
            mantain_list[state] = True
            return False

        remove_trans = []
        for out_trans, next in state.nexts.items():
            if not remove_list.get(next):
                arc = (state, out_trans.name, next)
                if not forbidden.get(arc):
                    forbidden[arc] = True
                    if mantain_list.get(next) or not \
                            self._prune_recursion(next, forbidden,
                                                  mantain_list, remove_list):
                        if not mantain_list.get(state):
                            mantain_list[state] = True
                        for trans in remove_trans:
                            del state.nexts[trans]
                        return False
                    else:
                        remove_trans.append(out_trans)

        remove_list[state] = True
        return True

    def dict_per_json(self):
        return {
            'space_state': [
                space_state.dict_per_json()
                for space_state in self._space_states
            ]
        }
