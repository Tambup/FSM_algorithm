import unittest
import select
import sys
from userInputOutput import UserInputOutput as UserIO
from ComportamentalFANSpace import ComportamentalFANSpace
from SpaceState import SpaceState


class TestStringMethods(unittest.TestCase):
    def test_maintain(self):
        f = open("sample/FSCNetwork.sample.json", "r")
        lines = [line.strip() for line in f]
        cfaNetwork = UserIO.readInput(''.join(line for line in lines))
        a = cfaNetwork._comportamentalFAs[0]._states[0]
        b = cfaNetwork._comportamentalFAs[1]._states[0]
        check = SpaceState([a, b], {'L2', 'L3'})
        test = ComportamentalFANSpace(cfaNetwork)
        test.build()
        self.assertTrue(test._space_states.__contains__(check))


if __name__ == '__main__':
    unittest.main()
