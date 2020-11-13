import copy
from core.OutTransition import OutTransition
from LOSpaceState import LOSpaceState


class Diagnosis:
    final_trans = OutTransition(name='',
                                destination='FINAL',
                                links=[],
                                observable=None,
                                relevant=None)

    final_state = LOSpaceState(states=[], links=[])

    def __init__(self, space_states):
        self._space_states = space_states
        self._work_space = None
        self._prev = None
        self._regex = ''
        self._temp = None

    @property
    def regex(self):
        return self._regex

    def diagnosis(self):
        self._unify_exit()
        while len(self._work_space) > 2:
            if self._sequence_transition():
                self._concat()
            elif self._set_parallel_tansition():
                self._attach()
            else:
                self._autotransition()  # Not sure if usefull

        self._regex = ''.join([
            tr.relevant for space in self._work_space.keys()
            for tr in space.nexts.keys()])

    def _unify_exit(self):
        self._work_space = {k: None for k in copy.deepcopy(self._space_states)}
        final_st = [state for state in self._work_space.keys()
                    if state.is_final()]
        for state in final_st:
            state.add_next(Diagnosis.final_trans, Diagnosis.final_state)

        self._work_space[Diagnosis.final_state] = None
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

    def _set_parallel_tansition(self):
        for state in self._work_space.keys():
            for trns, next_st in state.nexts.items():
                self._temp = (state, [trns], next_st)
                for trns_1, next_st_1 in state.nexts.items():
                    if trns is not trns_1 and next_st == next_st_1:
                        self._temp[1].append(trns_1)
                if len(self._temp[1]) > 1:
                    return True

    def _concat(self):
        rel = ''.join([rel if rel else ''
                       for _, _, rel in self._temp[:-1]])

        new_tr = OutTransition(name='',
                               destination=None,
                               links=[],
                               observable=None,
                               relevant=rel)
        self._temp[0][0].update_nexts(
                                     del_tr=[self._temp[0][1]],
                                     new_tr=new_tr,
                                     new_next=self._temp[-1])
        for i, elem in enumerate(self._prev[self._temp[-1]]):
            if elem == self._temp[-2][0]:
                self._prev[self._temp[-1]][i] = self._temp[0][0]
                break
        for elem, _, _ in self._temp[1:-1]:
            del self._work_space[elem]

    def _attach(self):
        rel = '(' + '|'.join(
            [tr.relevant if tr.relevant else LOSpaceState.NULL_EVT
                for tr in self._temp[1]]
            ) + ')'

        new_tr = OutTransition(name='',
                               destination=None,
                               links=[],
                               observable=None,
                               relevant=rel)
        self._temp[0].update_nexts(
                                   del_tr=self._temp[1],
                                   new_tr=new_tr,
                                   new_next=self._temp[-1])

        self._prev[self._temp[-1]] = [
            val for val in self._prev[self._temp[-1]] if val != self._temp[0]
            ]
        self._prev[self._temp[-1]].append(self._temp[0])

    def _autotransition(self):
        for state in self._work_space.keys():
            for trns, next_st in state.nexts.items():
                for fi_trns, fin_next_st in next_st.nexts.items():
                    auto_trans = next_st.auto_trans()
                    if auto_trans and auto_trans != fin_next_st:
                        autotr = f'({auto_trans.relevant})*'
                        self._temp = []
                        self._temp.append((
                            state,
                            trns,
                            (trns.relevant if trns.relevant else '') + autotr))
                        self._temp.append((next_st, fi_trns, fi_trns.relevant))
                        self._temp.append(fin_next_st)
                        self._concat()

    def _concat_auto_trans(self):
        rel = ''.join([
            self._temp[0][2] if self._temp[0][2] else '',
            self._temp[1],
            self._temp[2][2] if self._temp[2][2] else ''])
        print(rel)

    def dict_per_json(self):
        return {'regex': self._regex}
