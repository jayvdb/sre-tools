from __future__ import unicode_literals

import sre_compile
import sre_parse
import unittest

from sre_tools.utils import create_subpattern, clone_subpattern
from sre_tools._simplify import _val_eq


class TestCreateRegex(unittest.TestCase):
    def test_clone_basic(self):
        orig = sre_parse.parse(r"a{2}")
        new = clone_subpattern(orig)
        sre_compile.compile(new)
        assert _val_eq(orig, new)

    def test_create_basic(self):
        orig = sre_parse.parse(r"a{2}")
        new = create_subpattern(orig.data)
        sre_compile.compile(new)
        assert _val_eq(orig, new)
