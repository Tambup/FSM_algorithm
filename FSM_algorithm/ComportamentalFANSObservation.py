from ComportamentalFANSpace import ComportamentalFANSpace
from LOSpaceState import LOSpaceState


class ComportamentalFANSObservation(ComportamentalFANSpace):
    def __init__(self, compFAN):
        super().__init__(compFAN)
        self._id_count = None

    def build(self, param):
        super()._initialize()

        self._dfs_visit(self._space_states[0], obs=param, obs_index=0)

        mantain_dict = {}
        self._prune(self._space_states[0], mantain_dict)
        self._space_states = list(mantain_dict)

    def _dfs_visit(self, next_state, obs, obs_index):
        next_state.id = self._id_count
        self._id_count += 1
        next_state.obs_index = obs_index

        obs_val = obs[0] if obs else None
        next_trans = next_state.next_transition_state(obs_val)
        new_sp_states = self._get_nexts(next_state, next_trans, obs_val)

        for el, was_obs in new_sp_states:
            self._space_states.append(el)
            self._dfs_visit(el, obs[1:], obs_index+1) if was_obs \
                else self._dfs_visit(el, obs, obs_index)

    def _get_nexts(self, space_state, next_transition, obs):
        num_comp_FA = 0
        nexts = []
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

                    nexts.append(
                        (new_spc_st, (obs in actual_out_trans.observable))
                    )
                    if obs:
                        space_state.has_next_obs()
                    space_state.add_next(actual_out_trans, new_spc_st)
            except KeyError:
                pass
            num_comp_FA += 1
        return nexts

    def _init_instance(self, init_states, link_names):
        self._id_count = 0
        return [LOSpaceState(init_states, link_names)]

    def _prune(self, actual_state, mantain_list):
        reach_final = False
        if actual_state.is_final():
            mantain_list[actual_state] = True
            reach_final = True

        remove_list = []
        for trans, next in actual_state.nexts.items():
            if self._prune(next, mantain_list):
                if not reach_final:
                    mantain_list[actual_state] = True
                    reach_final = True
            else:
                remove_list.append(trans)

        if reach_final:
            for trans in remove_list:
                del actual_state.nexts[trans]

        return reach_final

    def dict_per_json(self):
        return {
            'space_state_linear_observation': [
                space_state.dict_per_json()
                for space_state in self._space_states
            ]
        }