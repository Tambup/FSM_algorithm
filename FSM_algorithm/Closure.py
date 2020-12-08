from core.SubscriptedTransition import SubscriptedTransition as SubscrTrans
from SpaceState import SpaceState
from RegexOperation import RegexOperation
from DetachedNextsSpaceState import DetachedNextsSpaceState as DNSpaceState


class Closure(RegexOperation):
    final_state = DNSpaceState(SpaceState(states=['', ''], links=[]))

    def __init__(self, enter_state_index, state_space, name):
        super().__init__()
        self._name = name
        self._init_index = enter_state_index
        self._init_space = state_space
        self._to_decorate = None
        self._final_states = None
        self._exit_states = None
        self._regex = ''
        self._out = None

    @property
    def name(self):
        return self._name

    @property
    def regex(self):
        return self._regex

    def is_final(self):
        return True if self._final_states else False

    def in_space_state(self):
        return DNSpaceState(self._init_space[self._init_index])

    def build(self):
        init_st = DNSpaceState(space_state=SpaceState(states=[''], links=[]),
                               is_closure_init=True)
        init_st.set_link(SpaceState.NULL_EVT, '!'+SpaceState.NULL_EVT)
        trans = SubscrTrans(name='', destination='INITIAL', links=[],
                            observable=None, relevant=None)
        init_st.add_next(transition=trans,
                         next=DNSpaceState(self._init_space[self._init_index]))
        temp = [init_st]
        self._work_space = {temp[0]: None}

        self._to_decorate = {}
        self._final_states = {}
        self._exit_states = {}

        grey_list = {temp[0]: temp[0]}
        for state in temp:
            new_nexts = {}
            for next_trans, next_state in state.nexts.items():
                new_state = None
                new_state = DNSpaceState(space_state=next_state)
                new_trans = SubscrTrans.from_trans(out_trans=next_trans)
                new_nexts[new_trans] = new_state
                if not self._work_space.get(next_state):
                    if not new_trans.observable:
                        self._work_space[new_state] = None
                        if grey_list.get(new_state):
                            new_nexts[new_trans] = grey_list[new_state]
                        else:
                            temp.append(new_state)
                grey_list[new_state] = new_state

            state.nexts = new_nexts
            if state.to_decorate():
                self._to_decorate[state] = None
            if state.is_final():
                self._final_states[state] = -100
            if state.exit_state():
                self._exit_states[state] = -100
        self._decorate()

    def _decorate(self):
        self._unify_exit()
        while len(self._work_space) > 2:
            if super()._sequence_transition():
                super()._concat(self._temp[-2][1].subscript_value)
            elif super()._set_parallel_tansition(subscripted=True):
                super()._alternative(null_evt=DNSpaceState.NULL_EVT)
            else:
                self._remaining()

        to_join = [tr for space in self._work_space.keys()
                   for tr in space.nexts.keys()
                   if tr.subscript_value in self._final_states.keys()]
        self._regex = '|'.join([tr.relevant if tr.relevant
                                else SpaceState.NULL_EVT
                                for tr in to_join])

        self._exit_states = self._build_exit_regex()
        if not self._regex:
            self._regex = SpaceState.NULL_EVT

    def _build_exit_regex(self):
        temp = {}
        for space in self._work_space.keys():
            for tr in space.nexts.keys():
                if tr.subscript_value in self._exit_states.keys():
                    if temp.get(self._exit_states[tr.subscript_value]) is None:
                        if tr.relevant:
                            temp[self._exit_states[tr.subscript_value]] \
                                = tr.relevant
                        else:
                            temp[self._exit_states[tr.subscript_value]] \
                                = SpaceState.NULL_EVT
                    else:
                        if tr.relevant:
                            temp[self._exit_states[tr.subscript_value]] \
                                += '|' + tr.relevant
                        else:
                            temp[self._exit_states[tr.subscript_value]] \
                                += '|' + SpaceState.NULL_EVT
        return temp

    def _unify_exit(self):
        for i, state in enumerate(self._to_decorate.keys()):
            trans = SubscrTrans(name='',
                                destination='FINAL',
                                links=[],
                                observable=None,
                                relevant=None,
                                subscr=i)
            if self._final_states.get(state):
                self._final_states[i] = state
            if self._exit_states.get(state):
                self._exit_states[i] = state
            state.add_next(trans, Closure.final_state)

        self._work_space[Closure.final_state] = None
        self._prev = {}
        for state in self._work_space.keys():
            self._prev[state] = []
        for state in self._work_space.keys():
            for _, next_st in state.nexts.items():
                self._prev[next_st].append(state)

    def _new_generic_trans_given_relevance(self, relevance, nk=None):
        return SubscrTrans(name='',
                           destination=None,
                           links=[],
                           observable=None,
                           relevant=relevance,
                           subscr=nk)

    def build_next(self, closures):
        self._out = {}
        for state in self._exit_states.keys():
            for trns in state.external_nexts.keys():
                self._out[trns.observable] = []

        for state, regex in self._exit_states.items():
            for trns, succ in state.external_nexts.items():
                for closure in closures:
                    if succ == closure.in_space_state():
                        trns_regex = trns.relevant if trns.relevant else ''
                        trns_regex = regex + trns_regex
                        self._out[trns.observable].append(
                            {
                                'successor': closure,
                                'trns_regex': trns_regex
                            }
                        )
                        break

    def out_list(self, observation):
        return self._out.get(observation, [])

    def dict_per_json(self):
        temp = {}
        temp['name'] = self._name
        temp['in_state_id'] = self.in_space_state().id
        temp['regex'] = self._regex
        inner_temp = {}
        for o, out_list in self._out.items():
            inner_temp[o] = []
            for out in out_list:
                inner_temp[o].append(
                    {
                        'successor': out['successor'].name,
                        'trns_regex': out['trns_regex']
                    })

        temp['exit'] = inner_temp
        return temp
