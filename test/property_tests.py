# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from string import lower
from google.appengine.ext import ndb
from ndbext.property import IntegerBoundary, BoundaryError
from util import GAETestCase


class IntegerModelMock(ndb.Model):
    lower = IntegerBoundary(lower=0)
    upper = IntegerBoundary(upper=3)
    lower_and_upper = IntegerBoundary(lower=-1, upper=1)


class IntegerBoundaryTests(GAETestCase):
    def test_lower(self):
        self.assertRaises(BoundaryError, IntegerModelMock, lower=-1)

        # no exceptions with bigger values
        IntegerModelMock(lower=0)
        IntegerModelMock(lower=99999999999999999999)
    def test_lower_and_upper(self):
        self.assertRaises(BoundaryError, IntegerModelMock, lower_and_upper=-3)
        self.assertRaises(BoundaryError, IntegerModelMock, lower_and_upper=2)

        # no exceptions with values in interval
        IntegerModelMock(lower=0)

    def test_upper(self):
        self.assertRaises(BoundaryError, IntegerModelMock, upper=4)

        # no exceptions with bigger values
        IntegerModelMock(upper=3)
        IntegerModelMock(upper=-99999999999999999999)

    def test_none(self):
        #asserting nothing hapens with None values
        IntegerModelMock(lower=None,upper=None,lower_and_upper=None)


