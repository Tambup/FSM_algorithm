import copy
from Task import Task
from SpaceState import SpaceState


class ComportamentalFANSpace(Task):
    def __init__(self, compFAN):
        super().__init__(compFAN)
        self._space_states = []

    def build(self):
        self._initialize()

        index = 0
        while (index < len(self._space_states)):
            actual_space_state = self._space_states[index]
            next_trans_state = actual_space_state.next_transition_state()
            self._add_states(actual_space_state, next_trans_state)
            index += 1

        self._prune()

    def _initialize(self) -> SpaceState:
        compFAs = super().compFAN.comportamentalFAs
        link_names = super().compFAN.in_links()
        init_states = [compFA.init_state() for compFA in compFAs]
        init = SpaceState(init_states, link_names)
        self._space_states = [init]

    def _add_states(self, space_state, next_transition):
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
                        self._space_states.append(new_spc_st)
                        space_state.add_next(actual_out_trans, new_spc_st)
            except KeyError:
                pass
            num_comp_FA += 1

    def _prune(self):
        pass

    def _new_state(self, old_space, old_state, new_state, out_trans):
        new_space = copy.deepcopy(old_space)
        for link_name, link_type, link_event in out_trans.links:
            if link_type == "out":
                new_space.set_link(link_name, link_event)
            else:
                new_space.clear_link(link_name)

        new_space.change_state(old_state, new_state)
        return new_space
