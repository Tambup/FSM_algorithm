from ComportamentalFANSpace import ComportamentalFANSpace
from LOSpaceState import LOSpaceState
import functools


class ComportamentalFANSObservation(ComportamentalFANSpace):
    def __init__(self, compFAN):
        super().__init__(compFAN)
        self._observation = None
        self._id_count = None

    def build(self, observation):
        self._observation = observation
        print('\nStart creation CFANS on observation ' +
              str(observation) + '\n')
        super()._initialize()
        self._dfs_visit(next_state=self._space_states[0],
                        obs=observation,
                        obs_index=0,
                        grey_list={})
        mantain_dict = {}
        remove_list = []
        self._prune(self._space_states[0], mantain_dict, remove_list)
        for act_st, trns, nx_st in remove_list:
            if not mantain_dict.get(nx_st):
                print('pruned state number ' + str(act_st.nexts[trns].id))
                del act_st.nexts[trns]

        self._space_states = list(mantain_dict)
        print('\nCFANS respect observation ' + str(observation) + ' complete')

    def _dfs_visit(self, next_state, obs, obs_index, grey_list):
        next_state.id = self._id_count
        print('add new state number ' + str(self._id_count))
        self._id_count += 1
        next_state.obs_index = obs_index
        grey_list[next_state] = True

        obs_val = obs[0] if obs else None
        next_trans = next_state.next_transition_state(obs_val)
        new_sp_states = self._get_nexts(next_state, next_trans, obs_val)

        for el, obs_used in new_sp_states:
            if not grey_list.get(el):
                self._space_states.append(el)
                if obs_used:
                    self._dfs_visit(el, obs[1:], obs_index+1, grey_list)
                else:
                    self._dfs_visit(el, obs, obs_index, grey_list)

        del grey_list[next_state]

    def _get_nexts(self, space_state, next_transition, obs):
        nexts = []
        for changing_state in next_transition.keys():
            i, actual_out_trans_list = next_transition[changing_state]
            for actual_out_trans in actual_out_trans_list:
                for candidate in super().compFAN.comportamentalFAs[i].states:
                    if actual_out_trans.destination == candidate.name:
                        new_spc_st = self._new_state(space_state,
                                                     changing_state,
                                                     candidate,
                                                     actual_out_trans)

                        nexts.append((new_spc_st, obs
                                     and obs == actual_out_trans.observable))
                        space_state.set_has_obs(False if obs is None else True)
                        space_state.add_next(actual_out_trans, new_spc_st)
                        break
        return nexts

    def _init_instance(self, init_states, link_names):
        self._id_count = 0
        return [LOSpaceState(init_states, link_names)]

    def _prune(self, actual_state, mantain_list, remove_list):
        reach_final = False
        if actual_state.is_final():
            mantain_list[actual_state] = True
            reach_final = True

        for trans, next in actual_state.nexts.items():
            if self._prune(next, mantain_list, remove_list):
                if not reach_final:
                    mantain_list[actual_state] = True
                    reach_final = True
            else:
                remove_list.append((actual_state, trans, next))

        return reach_final

    def dict_per_json(self):
        num_trans = 0
        for space_state in self._space_states:
            num_trans += len(space_state._nexts)
        return {
            'observation': self._observation,
            'number comportamental FA': len(super().compFAN.comportamentalFAs),
            'number states': functools.reduce(
                lambda old, new: old+new,
                [len(fa.states) for fa in super().compFAN.comportamentalFAs]),
            'number space states': len(self._space_states),
            'number transitions': num_trans,
            'space_state_linear_observation': [
                space_state.dict_per_json()
                for space_state in self._space_states
            ]
        }
