import unittest
from core.ComportamentalFANetwork import ComportamentalFANetwork


class TestStringMethods(unittest.TestCase):
    def test_valid_check(self):
        compFa = {
            'name': 'C2',
            'state': [{
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
                ]}, {
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
                ]}, {
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
            ]}
        compFan = ComportamentalFANetwork('Mesto', [compFa])
        self.assertTrue(compFan.check())

    def test_check_null_comportamental_FAs(self):
        compFa = {
            'name': None,
            'state': []}
        compFan = ComportamentalFANetwork('Mesto', [compFa])
        self.assertFalse(compFan.check())

    def test_null_comportamental_FA(self):
        compFa = {
            'name': 'C2',
            'state': [{
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
                ]}, {
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
            ]}
        compFan = ComportamentalFANetwork('Mesto', [compFa])
        self.assertFalse(compFan.check())

    def test_check_correct_links(self):
        compFa1 = {
            'name': 'C2',
            'state': [{
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
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L6",
                        "event": "e7"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L6",
                        "event": "e7"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L6",
                        "event": "e7"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}

        compFa2 = {
            'name': 'C3',
            'state': [{
                'name': '25',
                'init': True,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '26',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '26',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L6",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '27',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L6",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}
        compFan = ComportamentalFANetwork('Mesto', [compFa1, compFa2])
        self.assertTrue(compFan.check())

    def test_check_links_go_nowhere(self):
        compFa1 = {
            'name': 'C2',
            'state': [{
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
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L6",
                        "event": "e7"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L6",
                        "event": "e7"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L6",
                        "event": "e7"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}

        compFa2 = {
            'name': 'C3',
            'state': [{
                'name': '25',
                'init': True,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '26',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '26',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '27',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}
        compFan = ComportamentalFANetwork('Mesto', [compFa1, compFa2])
        self.assertFalse(compFan.check())

    def test_check_auto_link_doesnt_count(self):
        compFa1 = {
            'name': 'C2',
            'state': [{
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
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}
        compFa2 = {
            'name': 'C3',
            'state': [{
                'name': '25',
                'init': True,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '26',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L5",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '26',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"}, {
                        "type": "in",
                        "link": "L5",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '27',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"}, {
                        "type": "in",
                        "link": "L5",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}
        compFan = ComportamentalFANetwork('Mesto', [compFa1, compFa2])
        self.assertFalse(compFan.check())

    def test_check_link_from_nowhere(self):
        compFa1 = {
            'name': 'C2',
            'state': [{
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
                        "link": "L6",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L6",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
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
                        "link": "L6",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}
        compFa2 = {
            'name': 'C3',
            'state': [{
                'name': '25',
                'init': True,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '26',
                    'link': [{
                        "type": "in",
                        "link": "L5",
                        "event": "e3"},
                        {
                        "type": "out",
                        "link": "L2",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '26',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L6",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}, {
                'name': '27',
                'init': False,
                'outTransition': [{
                    'name': 't2a',
                    'destination': '27',
                    'link': [{
                        "type": "in",
                        "link": "L6",
                        "event": "e3"}],
                    'observable': [],
                    'relevant': []}
                ]}
            ]}
        compFan = ComportamentalFANetwork('Mesto', [compFa1, compFa2])
        self.assertFalse(compFan.check())


if __name__ == '__main__':
    unittest.main()
