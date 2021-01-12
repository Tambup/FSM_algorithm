"""
This module contains all the classes that, appropriately linked, constitute
a FA network.

| The classes are listed in order such that the first contains the second,
  the second contains the third and so on.
| An exception is **SubscriptedTransition**, that is subclass of OutTransition.
"""
from .ComportamentalFA import ComportamentalFA
from .ComportamentalFANetwork import ComportamentalFANetwork
from .OutTransition import OutTransition
from .State import State
from .SubscriptedTransition import SubscriptedTransition

__all__ = ['ComportamentalFA',
           'ComportamentalFANetwork',
           'OutTransition',
           'State',
           'SubscriptedTransition']
