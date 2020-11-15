from core.OutTransition import OutTransition
from SpaceState import SpaceState
from DetachedNextsSpaceState import DetachedNextsSpaceState as DNSpaceState


class Closure:
    final_trans = OutTransition(name='',
                                destination='FINAL',
                                links=[],
                                observable=None,
                                relevant=None)

    final_state = SpaceState(states=[], links=[])

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
                new_state = DNSpaceState(next_state)
                new_nexts[next_trans] = next_state
                if not self._work_space.get(next_state):
                    if not next_trans.observable:
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
                pass

    def _unify_exit(self):
        for state in self._finals.keys():
            state.add_next(Closure.final_trans, Closure.final_state)

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
