import copy
import functools
from .Task import Task
from .SpaceState import SpaceState


class ComportamentalFANSpace(Task):
    """
    The class rapresent a comportamental finite automa network space.

    From now comportamental finite automa network space are identified
    as CFANS.

    :param compFAN: The comportamental FA network
    :type compFAN: :class:`~FSM_algorithm.core.ComportamentalFANetwork`
    """
    def __init__(self, compFAN):
        """
        Constructor method.
        """
        super().__init__(compFAN)
        self._space_states = []

    @property
    def space_states(self):
        """
        Returns all the :class:`~FSM_algorithm.SpaceState.SpaceState`
        of the current Comportamental FAN Space.

        :return: The list of :class:`~FSM_algorithm.SpaceState.SpaceState`
        :rtype: list
        """
        return self._space_states

    def is_correct(self):
        """
        Check if the Compotamental FAN Space is corret or not.

        :return: True if is correct, else false
        :rtype: bool
        """
        return True if self._space_states else False

    def build(self, param=None):
        """
        Build a CFANS pruning states that cannot reach a final state.

        :param param: In this class is useless. Don't use it, defaults to None
        :type param: list, optional
        """
        print('Start creation CFANS\n')
        self._initialize()
        id = 1
        present = {st: st for st in self._space_states}
        for actual_space_state in self._space_states:
            print('add new state number ' + str(actual_space_state._id))
            next_trans_state = actual_space_state.next_transition_state()
            id = self._add_states(space_state=actual_space_state,
                                  next_transition=next_trans_state,
                                  present=present,
                                  id=id)
        self._prune()
        print('\nCFANS complete')

    def build_no_prune(self, param=None):
        """
        Build a CFANS without pruning.

        :param param: In this class is useless. Don't use it, defaults to None
        :type param: list, optional
        """
        self._initialize()

        id = 1
        present = {st: st for st in self._space_states}
        for actual_space_state in self._space_states:
            next_trans_state = actual_space_state.next_transition_state()
            id = self._add_states(space_state=actual_space_state,
                                  next_transition=next_trans_state,
                                  present=present,
                                  id=id)

    def _init_instance(self, init_states, link_names):
        return [SpaceState(init_states, link_names)]

    def _initialize(self):
        compFAs = super().compFAN.comportamentalFAs
        link_names = super().compFAN.in_links()
        init_states = [compFA.init_state() for compFA in compFAs]
        self._space_states = self._init_instance(init_states, link_names)
        self._space_states[0].id = 0

    def _add_states(self, space_state, next_transition, id, present):
        for changing_state in next_transition.keys():
            i, actual_out_trans_list = next_transition[changing_state]
            for actual_out_trans in actual_out_trans_list:
                for candidate in super().compFAN.comportamentalFAs[i].states:
                    if actual_out_trans.destination == candidate.name:
                        new_spc_st = self._new_state(space_state,
                                                     changing_state,
                                                     candidate,
                                                     actual_out_trans)
                        try:
                            space_state.add_next(actual_out_trans,
                                                 present[new_spc_st])
                        except KeyError:
                            new_spc_st.id = id
                            id += 1
                            self._space_states.append(new_spc_st)
                            present[new_spc_st] = new_spc_st
                            space_state.add_next(actual_out_trans, new_spc_st)
                        break
        return id

    def _new_state(self, old_space, old_state, new_state, out_trans):
        new_space = copy.deepcopy(old_space)
        for link_name, link_type, link_event in out_trans.links:
            if link_type == 'out':
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
        for rm_state in remove_list.keys():
            print('prune state number ' + str(rm_state.id))
            for st in self._space_states:
                rm_trans = []
                for trns, nx in st.nexts.items():
                    if nx == rm_state:
                        rm_trans.append(trns)
                for trns in rm_trans:
                    print('prune transition from ' + str(st.id)
                          + ' to ' + str(rm_state.id))
                    del st.nexts[trns]
        self._space_states = list(mantain_list.keys())

    def _prune_recursion(self, state, forbidden, mantain_list, remove_list):
        if state.is_final():
            mantain_list[state] = True
            return False

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
                            if remove_list.get(state):
                                del remove_list[state]
                        return False
        if not mantain_list.get(state):
            remove_list[state] = True
        return True

    def dict_per_json(self):
        """
        Returns the object's attributes in a form easy to transform in json.

        :return: All the necessary information in a data structure
        :rtype: dict
        """
        num_trans = 0
        for space_state in self._space_states:
            num_trans += len(space_state._nexts)
        return {
            'number comportamental FA': len(super().compFAN.comportamentalFAs),
            'number states': functools.reduce(
                lambda old, new: old+new,
                [len(fa.states) for fa in super().compFAN.comportamentalFAs]),
            'number space states': len(self._space_states),
            'number transitions': num_trans,
            'space_state': [
                space_state.dict_per_json()
                for space_state in self._space_states
            ]
        }
