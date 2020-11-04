import unittest
from core.ComportamentalFA import ComportamentalFA


class TestStringMethods(unittest.TestCase):
    def test_check_no_init_state(self):
        state1 = {
            'name': '21',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}, {
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e2"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1])
        self.assertFalse(compFa.check())

    def test_check_init_state(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}, {
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e2"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1])
        self.assertTrue(compFa.check())

    def test_check_multiple_init_state(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}, {
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e2"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}, {
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e2"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2])
        self.assertFalse(compFa.check())

    def test_check_is_not_isolated(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2])
        self.assertTrue(compFa.check())

    def test_check_is_isolated(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': []}
        compFa = ComportamentalFA('C2', [state1, state2])
        self.assertFalse(compFa.check())

    def test_check_is_isolated_only_loop(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2])
        self.assertFalse(compFa.check())

    def test_check_is_isolated_only_no_enter(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state3 = {
            'name': '23',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2, state3])
        self.assertTrue(compFa.check())

    def test_check_is_isolated_only_no_exit(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '23',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state3 = {
            'name': '23',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '23',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2, state3])
        self.assertTrue(compFa.check())

    def test_check_out_transition_destination_no_exists(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '25',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '23',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state3 = {
            'name': '23',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '23',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2, state3])
        self.assertFalse(compFa.check())

    def test_check_duplicate_name(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state3 = {
            'name': '21',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2, state3])
        self.assertFalse(compFa.check())

    def test_check_null_states(self):
        state1 = {
            'name': None,
            'init': None,
            'outTransition': []}
        compFa = ComportamentalFA('C2', [state1])
        self.assertFalse(compFa.check())

    def test_check_null_state(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '22',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state3 = {
            'name': None,
            'init': None,
            'outTransition': []}
        compFa = ComportamentalFA('C2', [state1, state2, state3])
        self.assertFalse(compFa.check())

    def test_check_duplicate_state(self):
        state1 = {
            'name': '21',
            'init': True,
            'outTransition': [{
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}, {
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e2"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        state2 = {
            'name': '21',
            'init': False,
            'outTransition': [{
                'name': 't2a',
                'destination': '21',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e3"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}, {
                'name': 't2a',
                'destination': '22',
                'link': [{
                    "type": "in",
                    "link": "L2",
                    "event": "e2"},
                    {
                    "type": "out",
                    "link": "L3",
                    "event": "e3"}],
                'observable': [],
                'relevant': []}
            ]}
        compFa = ComportamentalFA('C2', [state1, state2])
        self.assertFalse(compFa.check())


if __name__ == '__main__':
    unittest.main()
