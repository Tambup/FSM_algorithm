import unittest
import select
import sys
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from core.ComportamentalFANetwork import ComportamentalFANetwork
from core.OutTransition import OutTransition
from SpaceState import SpaceState
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

    def test_add_state_valid(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace._initialize()
        ss = fanSpace._space_states[0]
        nt = ss.next_transition_state()
        transition = nt[ss.states[1]][0]
        fanSpace._add_states(ss, nt, 1)
        self.assertTrue(fanSpace._space_states[0]._nexts[transition] ==
                        fanSpace._space_states[1])

    def test_add_state_valid_no_dupplicate_state(self):
        f = open('sample/FSCNetwork.sample.json', 'r')
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        fanSpace = ComportamentalFANSpace(cfaNetwork)
        fanSpace._initialize()
        fanSpace._add_states(fanSpace._space_states[0], fanSpace.
                             _space_states[0].next_transition_state(), 1)
        fanSpace._add_states(fanSpace._space_states[1], fanSpace.
                             _space_states[1].next_transition_state(), 2)
        fanSpace._add_states(fanSpace._space_states[2], fanSpace.
                             _space_states[2].next_transition_state(), 3)
        fanSpace._add_states(fanSpace._space_states[4], fanSpace.
                             _space_states[4].next_transition_state(), 5)
        fs_dim_l_it = len(fanSpace._space_states)
        fanSpace._add_states(fanSpace._space_states[5], fanSpace.
                             _space_states[5].next_transition_state(), 6)
        self.assertTrue(fanSpace._space_states[0]._states[0] in
                        fanSpace._space_states[5]._states and
                        fs_dim_l_it + 1 == len(fanSpace._space_states))


if __name__ == '__main__':
    unittest.main()
