# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb


class BoundaryError(Exception):
    pass


class IntegerBoundary(ndb.IntegerProperty):
    '''
    Property to define a bounded integer based on lower and upper values
    default value of properties is None and in this case no validation is executed
    '''
    def __init__(self, lower=None, upper=None, **kwargs):
        self.upper = upper
        self.lower = lower
        super(IntegerBoundary, self).__init__(**kwargs)

    def _validate(self, value):
        if self.lower is not None and value < self.lower:
            raise BoundaryError('%s is less then %s' % (value, self.lower))
        if self.upper is not None and value > self.upper:
            raise BoundaryError('%s is greater then %s' % (value, self.upper))
