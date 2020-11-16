from core.SubscriptedTransition import SubscriptedTransition as SubscrTrans
from SpaceState import SpaceState
from DetachedNextsSpaceState import DetachedNextsSpaceState as DNSpaceState


class Closure:
    final_state = DNSpaceState(SpaceState(states=[], links=[]))

    def __init__(self, enter_state_index, state_space):
        self._init_index = enter_state_index
        self._init_space = state_space
        self._work_space = None
        self._finals = None
        self._prev = None
        self._temp = None

    def build(self):
        self._init_space = [DNSpaceState(k) for k in self._init_space]
        temp = [DNSpaceState(self._init_space[self._init_index])]
        self._work_space = {temp[0]: None}

        self._finals = {}
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
            if state.is_final():
                self._finals[state] = None

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

    def _unify_exit(self):
        for i, state in enumerate(self._finals.keys()):
            trans = SubscrTrans(name='',
                                dest='FINAL',
                                links=[],
                                observable=None,
                                relevant=None,
                                subscr=i)
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
        for n_first in self._work_space.keys():
            for r_first, n in n_first.nexts.items():
                for r_second, n_second in n.nexts.items():
                    auto_trans = n.auto_trans()
                    self._temp = []
                    if auto_trans and auto_trans != n_second:
                        autotr = f'({auto_trans.relevant})*'
                        self._temp.append((
                            n_first,
                            r_first,
                            (r_first.relevant if r_first.relevant else '')
                            + autotr))
                        self._temp.append((n, r_second, r_second.relevant))
                        self._temp.append(n_second)
                        self._concat(self._temp[-2][1].subscript_value)
