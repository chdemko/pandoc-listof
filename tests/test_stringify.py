# This Python file uses the following encoding: utf-8
from unittest import TestCase
from pandocfilters import Str, Code, Math, LineBreak, Space, Note

import pandoc_listof

def init():
    pandoc_listof.collections = {}
    pandoc_listof.headers = [0, 0, 0, 0, 0, 0]

def test_Str():
    init()

    src = [Str(u'Exercise')]
    dest = u'Exercise'
    assert pandoc_listof.stringify(src, '') == dest
    assert pandoc_listof.stringify(src, 'latex') == dest

def test_Code():
    init()

    src = [Code(['', [], []], 'unsigned int')]
    dest = u'unsigned int'
    assert pandoc_listof.stringify(src, '') == dest
    assert pandoc_listof.stringify(src, 'latex') == dest

def test_Math():
    init()

    src = [Math({'t': 'InlineMath', 'c': []}, 'a=1')]
    dest = u'a=1'
    assert pandoc_listof.stringify(src, '') == dest

    dest = u'$a=1$'
    assert pandoc_listof.stringify(src, 'latex') == dest

def test_LineBreak():
    init()

    src = [LineBreak()]
    dest = u' '
    assert pandoc_listof.stringify(src, '') == dest
    assert pandoc_listof.stringify(src, 'latex') == dest

def test_Space():
    init()

    src = [Space()]
    dest = u' '
    assert pandoc_listof.stringify(src, '') == dest
    assert pandoc_listof.stringify(src, 'latex') == dest

def test_Note():
    init()

    src = [Note([Str(u'The'), Space(), Str(u'note')])]
    dest = u''
    assert pandoc_listof.stringify(src, '') == dest
    assert pandoc_listof.stringify(src, 'latex') == dest

