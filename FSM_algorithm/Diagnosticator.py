from .Closure import Closure
from .SpaceState import SpaceState


class Diagnosticator:
    def __init__(self, space_states):
        self._space_states = space_states
        self._closures = None
        self._regex = None
        self._is_linear_diagnosis = False
        self._observation = None

    def build(self):
        print('\nStart diagnosticator')
        self._build_closures()
        self._build_closure_space()

    def _build_closures(self):
        closable = {}
        for act in self._space_states:
            if act.is_init():
                closable[act] = None
            for trans, state in act.nexts.items():
                if trans.observable:
                    closable[state] = None
        closable = [self._space_states.index(elem) for elem in closable.keys()]
        self._closures = []
        for i, index in enumerate(closable):
            closure = Closure(enter_state_index=index,
                              state_space=self._space_states,
                              name='x'+str(i))
            closure.build()
            print('add new closure ' + closure._name)
            self._closures.append(closure)

    def _build_closure_space(self):
        for closure in self._closures:
            closure.build_next(self._closures)

    def linear_diagnosis(self, observations):
        print('\nStart evaluate diagnosis respect observation ' +
              str(observations))
        self._observation = observations
        self._is_linear_diagnosis = True
        X = {}
        for closure in self._closures:
            if closure.in_space_state().is_init():
                X[closure] = SpaceState.NULL_EVT
                break

        for o in observations:
            X_new = {}
            for x_first, rho_first in X.items():
                for arc in x_first.out_list(o):
                    x_second = arc['successor']
                    rho_second = self._build_rho_second(
                        first=rho_first,
                        second=arc['trns_regex']
                    )
                    X_new[x_second] = self._build_x_second_regex(
                        prev_val=X_new.get(x_second),
                        trns_regex=rho_second
                    )
            X = X_new

        X_new = {}
        for closure, regex in X.items():
            if closure.is_final():
                X_new[closure] = regex
        X = X_new

        if len(X) == 1:
            head = list(X.items())[0]
            self._regex = '(' + head[1] + ')(' + head[0].regex + ')'
        elif len(X) > 1:
            self._regex = ''
            for x, rho in X.items():
                self._regex += '(' + rho + '(' + x.regex + ')' + ')|'
            self._regex = self._regex[:-1]
        print(self._regex)

    def _build_rho_second(self, first, second):
        if first == SpaceState.NULL_EVT and second == SpaceState.NULL_EVT:
            return SpaceState.NULL_EVT
        elif first != SpaceState.NULL_EVT and second == SpaceState.NULL_EVT:
            return first
        elif first == SpaceState.NULL_EVT and second != SpaceState.NULL_EVT:
            return second
        else:
            return first + second

    def _build_x_second_regex(self, prev_val, trns_regex):
        if prev_val:
            if trns_regex not in prev_val.split('|'):
                return prev_val + '|' + trns_regex
            else:
                return prev_val
        else:
            return trns_regex

    def dict_per_json(self):
        if self._is_linear_diagnosis:
            return {
                'observation': self._observation,
                'number space states': len(self._space_states),
                'number closures': len(self._closures),
                'regex': self._regex
                }
        else:
            num_trans = 0
            for closure in self._closures:
                for out in closure._out.items():
                    num_trans += len(out[1])
            temp = {
                'number space states': len(self._space_states),
                'number closures': len(self._closures),
                'number transactions': num_trans
            }
            temp['closure'] = [
                closure.dict_per_json() for closure in self._closures
            ]
            return temp
