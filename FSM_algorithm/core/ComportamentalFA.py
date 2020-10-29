from core.State import State


class ComportamentalFA():
    def __init__(self, name, states):
        self._name = name
        self._states = []
        for state in states:
            self._states.append(State(name=state["name"],
                                is_init=state["init"],
                                out_transitions=state["outTransition"])
                                )

    @property
    def name(self):
        return self._name

    @property
    def states(self):
        return self._states

    def check(self):
        if self._states is None:
            return False
        if len(self._states) < 1:
            return False

        for state in self._states:
            if state is null:
                return False
            elif not state.check():
                return False

        init_counter = 0
        for state in self._states:
            if len(self._states) > 1:
                if state.no_exit() and _no_enter(state):
                    return False

            init_counter = init_counter+1 if state.is_init() else init_counter
            for inner_state in self._states:
                if state is not inner_state:
                    if state.name is None or inner_state.name in None:
                        return False
                    elif state.name == inner_state.name:
                        return False

            for out_trans in state.out_transition:
                must_continue = False
                for inner_state in self._states:
                    if out_trans.destination == inner_state.name:
                        must_continue = True
                        break

                if not must_continue:
                    return False

        return init_counter == 1

    def _no_enter(self, state):
        for inner_state in self._states:
            if state is not inner_state:
                if inner_state.out_transitions is not None:
                    for out_trans in inner_state.out_transitions:
                        if out_trans.destination == state.name:
                            return False

        return True