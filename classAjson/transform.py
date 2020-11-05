"""
Created by: David Bros
Date: 11/05/2020
Notes: This document lacks social distancing
"""

import types
import collections
import collections.abc
import functools
import operator
import re
import sys

class Transform(object):
    """
    Little test I did to ensure getattr and setitem are the correct methods
    """
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __setitem__(self, key, value):
        return object.__setattr__(self, key, value)

class MetaTransform(type):

    def __new__(mcs, classname, bases, classDict, *args):
        classDict['__len__'] = dict.__len__
        classDict['__getitem__'] = object.__getattribute__
        classDict['__setitem__'] = object.__setattr__
        classDict['__str__'] = mcs.tostr
        classDict['lattributes'] = mcs.lattributes
        classDict['lvalues'] = mcs.lvalues
        classDict['update'] = mcs.update
        classDict['fromdict'] = mcs.fromdict
        classDict['pop'] = mcs.popitem
        classDict['seq_update'] = mcs.seq_update
        classDict['nonseq_update'] = mcs.nonseq_update


        return super().__new__(mcs, classname, bases, classDict)

    def lattributes(cls):
        return list(cls.__dict__.keys())

    def lvalues(cls):
        return list(cls.__dict__.values())

    #Make a wrapper to use sequential/non sequential updates, right now it will be on a 2D iterable Iterable[Iterable[_KT, _VT]]
    #sequpdate(seq: set, list, dict...), nonsequpdate(name, value) -> None

    def seq_update(cls, iterable):
        for tup in iterable:
            cls.nonseq_update(tup)

    def nonseq_update(cls, non_iterable):
        return object.__setattr__(cls, non_iterable[0], non_iterable[1])

    def update(cls, iterable):
        """
        Update from a 2D sequence
        :param iterable:
        :return:
        """

        if type(iterable) == list:
            cls.seq_update(iterable)
        elif type(iterable) == dict:
            cls.seq_update(iterable.items())
        elif type(iterable) == tuple:
            cls.nonseq_update(iterable)
        else:
            raise TypeError("Type given to update is wrong, only iterators are allowed.")
        return True

    def tostr(cls):
        return cls.__dict__.__str__()

    def fromdict(cls, seq):
        for key, value in seq.items():
            object.__setattr__(cls, key, value)

    def popitem(cls, key=False):
        if key:
            return delattr(cls, key)

    #Future operations, such as joins, left joins, outer joins, inner joins and unions should be supported
    #Sort of a pythonic SQL like operations

class asdict(metaclass=MetaTransform):
    """
    asdict is meant to be inherited, making the metaclass propagate to your own classes (no community transmission tho)
    """
    pass

class generic(asdict):
    """
    Generic item for those who do not want the metaclass to propagate like covid-19
    """
    pass

__all__ = ['customObject', 'item']


