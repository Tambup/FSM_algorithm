from core.SubscriptedTransition import SubscriptedTransition as SubscrTrans
from SpaceState import SpaceState
from DetachedNextsSpaceState import DetachedNextsSpaceState as DNSpaceState


class Closure:
    final_state = DNSpaceState(SpaceState(states=[], links=[]))

    def __init__(self, enter_state_index, state_space, name):
        self._name = name
        self._init_index = enter_state_index
        self._init_space = state_space
        self._work_space = None
        self._to_decorate = None
        self._final_states = None
        self._exit_states = None
        self._prev = None
        self._temp = None
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
        temp = [DNSpaceState(self._init_space[self._init_index])]
        self._work_space = {temp[0]: None}

        self._to_decorate = {}
        self._final_states = {}
        self._exit_states = {}
        for state in temp:
            new_nexts = {}
            for next_trans, next_state in state.nexts.items():
                new_state = DNSpaceState(space_state=next_state)
                new_trans = SubscrTrans.from_trans(out_trans=next_trans)
                new_nexts[new_trans] = new_state
                if not self._work_space.get(next_state):
                    if not new_trans.observable:
                        self._work_space[new_state] = None
                        temp.append(new_state)
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
            if self._sequence_transition():
                self._concat(self._temp[-2][1].subscript_value)
            elif self._set_parallel_tansition():
                self._alternative()
            else:
                self._remaining()

        to_join = [tr for space in self._work_space.keys()
                   for tr in space.nexts.keys()
                   if tr.subscript_value in self._final_states.keys()]
        self._regex = '|'.join([tr.relevant if tr.relevant
                                else SpaceState.NULL_EVT
                                for tr in to_join])
        temp = {}
        for space in self._work_space.keys():
            for tr in space.nexts.keys():
                if tr.subscript_value in self._exit_states.keys():
                    if tr.relevant:
                        temp[self._exit_states[tr.subscript_value]] \
                            = tr.relevant
                    else:
                        temp[self._exit_states[tr.subscript_value]] \
                            = SpaceState.NULL_EVT
        self._exit_states = temp
        if not self._regex:
            self._regex = SpaceState.NULL_EVT

    def _unify_exit(self):
        for i, state in enumerate(self._to_decorate.keys()):
            trans = SubscrTrans(name='',
                                dest='FINAL',
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

    def _sequence_transition(self):
        for state in self._work_space.keys():
            for trns, next_st in state.nexts.items():
                self._temp = [(state, trns, trns.relevant)]
                index = 0
                remaining = [next_st]
                while index < len(remaining):
                    if len(remaining[index].nexts) == 1:
                        tr, succ = next(iter(remaining[index].nexts.items()))
                        self._temp.append((remaining[index], tr, tr.relevant))
                        remaining.append(succ)
                        if len(self._prev[succ]) > 1:
                            break

                    index += 1

                self._temp.append(remaining[-1])
                if len(self._temp) > 2:
                    return True

    def _concat(self, nk=None):
        rel = ''.join([rel if rel else ''
                       for _, _, rel in self._temp[:-1]])

        new_t = SubscrTrans(name='',
                            dest=None,
                            links=[],
                            observable=None,
                            relevant=rel,
                            subscr=nk)
        self._temp[0][0].update_nexts(del_tr=[self._temp[0][1]],
                                      new_tr=new_t,
                                      new_next=self._temp[-1])
        for i, elem in enumerate(self._prev[self._temp[-1]]):
            if elem == self._temp[-2][0]:
                self._prev[self._temp[-1]][i] = self._temp[0][0]
                break
        for elem, _, _ in self._temp[1:-1]:
            del self._work_space[elem]

    def _set_parallel_tansition(self):
        for state in self._work_space.keys():
            for trns, next_st in state.nexts.items():
                self._temp = (state, [trns], next_st)
                for trns_1, next_st_1 in state.nexts.items():
                    if trns is not trns_1 and next_st == next_st_1:
                        if trns.subscript_value == trns_1.subscript_value:
                            self._temp[1].append(trns_1)
                if len(self._temp[1]) > 1:
                    return True

    def _alternative(self):
        rel = '(' + '|'.join(
            [tr.relevant if tr.relevant else DNSpaceState.NULL_EVT
                for tr in self._temp[1]]
            ) + ')'

        new_tr = SubscrTrans(name='',
                             dest=None,
                             links=[],
                             observable=None,
                             relevant=rel,
                             subscr=self._temp[1][0].subscript_value)
        self._temp[0].update_nexts(del_tr=self._temp[1],
                                   new_tr=new_tr,
                                   new_next=self._temp[-1])

        self._prev[self._temp[-1]] = [
            val for val in self._prev[self._temp[-1]] if val != self._temp[0]
            ]
        self._prev[self._temp[-1]].append(self._temp[0])

    def _remaining(self):
        remove_val = None
        for n in self._work_space.keys():
            if remove_val:
                break
            for n_first in self._prev[n]:
                if n_first == n:
                    break
                for t_first, n_cand in n_first.nexts.items():
                    if n_cand == n:
                        break
                remove_next = False
                for t_second, n_second in n.nexts.items():
                    if n_second == n:
                        break
                    remove_val = n
                    remove_next = True
                    self._autotrans(first=(n_first, t_first, n),
                                    second=(n, t_second, n_second))
                if remove_next:
                    del n_first.nexts[t_first]
        if remove_val:
            for succ in remove_val.nexts.values():
                new_prev = []
                for i, sample in enumerate(self._prev[succ]):
                    if sample != remove_val:
                        new_prev.append(sample)
                self._prev[succ] = new_prev
            del self._work_space[remove_val]

    def _autotrans(self, first, second):
        autotr = None
        for t, n in second[0].nexts.items():
            if n == second[0]:
                autotr = t
                break
        autotr = autotr.relevant if autotr and autotr.relevant else ''
        rel1 = first[1].relevant if first[1].relevant else ''
        rel2 = second[1].relevant if second[1].relevant else ''
        if autotr:
            self._sub_trans(n_first=first[0],
                            rel=rel1 + f'({autotr})*' + rel2,
                            n_second=second[2],
                            nk=second[1].subscript_value)
        else:
            self._sub_trans(n_first=first[0],
                            rel=rel1 + rel2,
                            n_second=second[2],
                            nk=second[1].subscript_value)

    def _sub_trans(self, n_first, rel, n_second, nk):
        new_t = SubscrTrans(name='',
                            dest=None,
                            links=[],
                            observable=None,
                            relevant=rel,
                            subscr=nk)
        n_first.add_next(transition=new_t, next=n_second)
        self._prev[n_second].append(n_first)

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
                        trns_regex += regex
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
