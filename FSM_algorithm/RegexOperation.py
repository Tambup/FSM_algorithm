from core.SubscriptedTransition import SubscriptedTransition as SubscrTrans
from core.OutTransition import OutTransition
import stoppable


class RegexOperation:
    def __init__(self):
        self._temp = None
        self._work_space = None
        self._prev = None

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

    def _set_parallel_tansition(self, subscripted=None):
        for state in self._work_space.keys():
            for trns, next_st in state.nexts.items():
                self._temp = (state, [trns], next_st)
                for trns_1, next_st_1 in state.nexts.items():
                    if trns is not trns_1 and next_st == next_st_1:
                        if subscripted:
                            if trns.subscript_value == trns_1.subscript_value:
                                self._temp[1].append(trns_1)
                        else:
                            self._temp[1].append(trns_1)
                if len(self._temp[1]) > 1:
                    return True

    def _new_generic_trans_given_relevance(self, relevance, nk=None):
        raise NotImplementedError

    def _concat(self, nk=None):
        rel = ''.join([rel if rel else ''
                       for _, _, rel in self._temp[:-1]])

        new_tr = self._new_generic_trans_given_relevance(relevance=rel, nk=nk)

        self._temp[0][0].update_nexts(del_tr=[self._temp[0][1]],
                                      new_tr=new_tr,
                                      new_next=self._temp[-1])
        for i, elem in enumerate(self._prev[self._temp[-1]]):
            if elem == self._temp[-2][0]:
                self._prev[self._temp[-1]][i] = self._temp[0][0]
                break
        for elem, _, _ in self._temp[1:-1]:
            del self._work_space[elem]

    def _subscription_value(self, trns: OutTransition):
        return trns.subscript_value if isinstance(trns, SubscrTrans) else None

    def _alternative(self, null_evt):
        rel = '(' + '|'.join(
            [tr.relevant if tr.relevant else null_evt
                for tr in self._temp[1]]
            ) + ')'
        nk = self._subscription_value(self._temp[1][0])
        new_tr = self._new_generic_trans_given_relevance(relevance=rel, nk=nk)

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
        subscription = self._subscription_value(second[1])
        if autotr:
            self._sub_trans(n_first=first[0],
                            rel=rel1 + f'({autotr})*' + rel2,
                            n_second=second[2],
                            nk=subscription)
        else:
            self._sub_trans(n_first=first[0],
                            rel=rel1 + rel2,
                            n_second=second[2],
                            nk=subscription)

    def _sub_trans(self, n_first, rel, n_second, nk=None):
        new_t = self._new_generic_trans_given_relevance(relevance=rel, nk=nk)
        n_first.add_next(transition=new_t, next=n_second)
        self._prev[n_second].append(n_first)
