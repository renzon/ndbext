# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal
from google.appengine.ext import ndb


class BoundaryError(Exception):
    pass


class IntegerBounded(ndb.IntegerProperty):
    '''
    Property to define a bounded integer based on lower and upper values
    default value of properties is None and in this case no validation is executed
    '''

    def __init__(self, lower=None, upper=None, **kwargs):
        self.upper = upper
        self.lower = lower
        super(IntegerBounded, self).__init__(**kwargs)

    def _validate(self, value):
        if self.lower is not None and value < self.lower:
            raise BoundaryError('%s is less then %s' % (value, self.lower))
        if self.upper is not None and value > self.upper:
            raise BoundaryError('%s is greater then %s' % (value, self.upper))


class SimpleDecimal(IntegerBounded):
    '''
    Class representing a Decimal. It must be use when decimal places will never change
    decimal_places controls decimal places and its default is 2.
    Ex: decimal_places=2 -> 1.00, decimal_places=3 -> 1.000

    It's representation on db is Integer constructed from it values.
    Ex: decimal_places=2 -> 100, decimal_places=3 -> 1000

    This is useful so queries keep numeric meaning for comparisons like > or <=
    '''

    def __init__(self, decimal_places=2, lower=None, upper=None, **kwargs):
        self.decimal_places = decimal_places
        self.__multipler = (10 ** self.decimal_places)
        lower = lower and self._to_base_type(lower)
        upper = upper and self._to_base_type(upper)
        super(SimpleDecimal, self).__init__(lower=lower, upper=upper, **kwargs)

    def _validate(self, value):
        return Decimal(value)

    def _to_base_type(self, value):
        return int(round(Decimal(value) * self.__multipler))

    def _from_base_type(self, value):
        return Decimal(value) / self.__multipler


class SimpleCurrency(SimpleDecimal):
    def __init__(self, decimal_places=2, lower=0, **kwargs):
        super(SimpleCurrency, self).__init__(decimal_places=decimal_places,
                                             lower=lower,
                                             **kwargs)