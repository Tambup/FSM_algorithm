import unittest
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from core.State import State


class TestStringMethods(unittest.TestCase):
    def test_prune(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace.build_no_prune()
        a = fanSpace._space_states[13]
        b = fanSpace._space_states[14]
        fanSpace._prune()
        self.assertFalse(fanSpace._space_states.__contains__(a) or
                         fanSpace._space_states.__contains__(b))

    def test_prune_only_prunable(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace.build_no_prune()
        a = fanSpace._space_states[12]
        b = fanSpace._space_states[5]
        fanSpace._prune()
        self.assertTrue(a, b in fanSpace._space_states)

    def test_add_state_invalid(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace._initialize()
        fanSpace._add_states(fanSpace._space_states[0], fanSpace.
                             _space_states[0].next_transition_state(), 1,
                             {st: st for st in fanSpace.space_states})
        fanSpace._add_states(fanSpace._space_states[1], fanSpace.
                             _space_states[1].next_transition_state(), 2,
                             {st: st for st in fanSpace.space_states})
        fanSpace1 = ComportamentalFANSpace(cfaNetwork)
        fanSpace1._initialize()
        fanSpace1._add_states(fanSpace1._space_states[0], fanSpace1.
                              _space_states[0].next_transition_state(), 1,
                              {st: st for st in fanSpace1.space_states})
        fanSpace1._add_states(fanSpace1._space_states[1], fanSpace1.
                              _space_states[1].next_transition_state(), 2,
                              {st: st for st in fanSpace1.space_states})
        fanSpace1._add_states(fanSpace1._space_states[1], fanSpace1.
                              _space_states[0].next_transition_state(), 2,
                              {st: st for st in fanSpace1.space_states})
        self.assertFalse(fanSpace._space_states[1] !=
                         fanSpace1._space_states[1])

    def test_add_state_valid(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace._initialize()
        ss = fanSpace._space_states[0]
        nt = ss.next_transition_state()
        i, transition = nt[ss.states[1]]
        fanSpace._add_states(ss, nt, 1,
                             {st: st for st in fanSpace.space_states})
        self.assertTrue(fanSpace.space_states[0].nexts[transition[0]] ==
                        fanSpace.space_states[1])

    def test_add_state_valid_no_dupplicate_state(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace._initialize()
        fanSpace._add_states(fanSpace._space_states[0], fanSpace.
                             _space_states[0].next_transition_state(), 1,
                             {st: st for st in fanSpace.space_states})
        fanSpace._add_states(fanSpace._space_states[1], fanSpace.
                             _space_states[1].next_transition_state(), 2,
                             {st: st for st in fanSpace.space_states})
        fanSpace._add_states(fanSpace._space_states[2], fanSpace.
                             _space_states[2].next_transition_state(), 3,
                             {st: st for st in fanSpace.space_states})
        fanSpace._add_states(fanSpace._space_states[4], fanSpace.
                             _space_states[4].next_transition_state(), 5,
                             {st: st for st in fanSpace.space_states})
        fs_dim_l_it = len(fanSpace._space_states)
        fanSpace._add_states(fanSpace._space_states[5], fanSpace.
                             _space_states[5].next_transition_state(), 6,
                             {st: st for st in fanSpace.space_states})
        self.assertTrue(fanSpace._space_states[0]._states[0] in
                        fanSpace._space_states[5]._states and
                        fs_dim_l_it + 1 == len(fanSpace._space_states))

    def test_add_state_valid_expected_state(self):
        out_exp_1 = {
            'name': 't2a',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        out_exp_2 = {
            'name': 't3b',
            'destination': '30',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': None}
        out_exp_3 = {
            'name': 't3c',
            'destination': '31',
            'link': [{
                'type': 'in',
                'link': 'L3',
                'event': 'e3'}],
            'observable': None,
            'relevant': 'f'}
        state_exp_1 = State('20', True, [out_exp_1])
        state_exp_2 = State('31', False, [out_exp_2, out_exp_3])
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace._initialize()
        fanSpace._add_states(fanSpace._space_states[0], fanSpace.
                             _space_states[0].next_transition_state(), 1,
                             {st: st for st in fanSpace.space_states})
        self.assertTrue(state_exp_1, state_exp_2 in
                        fanSpace._space_states[1]._states and
                        len(fanSpace._space_states[1]._states) == 2)

    def test_add_state_invalid_expected_state(self):
        out_exp_1 = {
            'name': 't2c',
            'destination': '21',
            'link': [{
                'type': 'in',
                'link': 'L2',
                'event': 'e2'},
                {
                'type': 'out',
                'link': 'L3',
                'event': 'e3'}],
            'observable': 'o2',
            'relevant': None}
        state_exp_1 = State('20', True, [out_exp_1])
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace._initialize()
        fanSpace._add_states(fanSpace._space_states[0], fanSpace.
                             _space_states[0].next_transition_state(), 1,
                             {st: st for st in fanSpace.space_states})
        self.assertFalse(state_exp_1 in fanSpace._space_states[1]._states)


if __name__ == '__main__':
    unittest.main()
