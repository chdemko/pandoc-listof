# This Python file uses the following encoding: utf-8
from unittest import TestCase
from pandocfilters import Span, Str, Space, RawInline, Header

import json
import pandoc_listof

def init():
    pandoc_listof.collections = {}
    pandoc_listof.headers = [0, 0, 0, 0, 0, 0]

def test_classic():
    init()

    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    dest = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    assert pandoc_listof.collect(src['t'], src['c'], '', {}) == None
    assert src == dest
    assert pandoc_listof.collections == {'exercise': [{'identifier': u'1', 'text': u'Exercise 1'}]}

def test_headers():
    init()

    src = Header(1, [u'first-chapter', [], []], [Str(u'First'), Space(), Str('chapter')])
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})
    src = json.loads(json.dumps(Span(['exercise:2', [], []], [Str(u'Exercise'), Space(), Str(u'2')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = Header(1, [u'second-chapter', [], []], [Str(u'Second'), Space(), Str('chapter')])
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Span(['exercise:3', [], []], [Str(u'Exercise'), Space(), Str(u'3')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})
    src = json.loads(json.dumps(Span(['exercise:4', [], []], [Str(u'Exercise'), Space(), Str(u'4')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = Header(2, [u'first-section', [], []], [Str(u'First'), Space(), Str('section')])
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Span(['exercise:5', [], []], [Str(u'Exercise'), Space(), Str(u'5')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})
    src = json.loads(json.dumps(Span(['exercise:6', [], []], [Str(u'Exercise'), Space(), Str(u'6')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})

    assert pandoc_listof.collections == {
        'exercise': [
            {'identifier': u'1', 'text': u'Exercise 1'},
            {'identifier': u'2', 'text': u'Exercise 2'},
            {'identifier': u'3', 'text': u'Exercise 3'},
            {'identifier': u'4', 'text': u'Exercise 4'},
            {'identifier': u'5', 'text': u'Exercise 5'},
            {'identifier': u'6', 'text': u'Exercise 6'},
        ],
        'exercise:1': [
            {'identifier': u'1', 'text': u'Exercise 1'},
            {'identifier': u'2', 'text': u'Exercise 2'}
        ],
        'exercise:2': [
            {'identifier': u'3', 'text': u'Exercise 3'},
            {'identifier': u'4', 'text': u'Exercise 4'},
            {'identifier': u'5', 'text': u'Exercise 5'},
            {'identifier': u'6', 'text': u'Exercise 6'},
        ],
        'exercise:2.1': [
            {'identifier': u'5', 'text': u'Exercise 5'},
            {'identifier': u'6', 'text': u'Exercise 6'},
        ]
    }

def test_latex():
    init()

    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    latex = '\\phantomsection\\addcontentsline{exercise}{figure}{Exercise 1}'
    dest = json.loads(json.dumps(Span(['exercise:1', [], []], [RawInline('tex', latex), Str(u'Exercise'), Space(), Str(u'1')])))
    assert pandoc_listof.collect(src['t'], src['c'], 'latex', {}) == None
    assert json.loads(json.dumps(src)) == dest
    assert pandoc_listof.collections == {'exercise': [{'identifier': u'1', 'text': u'Exercise 1'}]}

def test_headers_latex():
    init()

    src = Header(1, [u'first-chapter', [], []], [Str(u'First'), Space(), Str('chapter')])
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    latex = '\\phantomsection\\addcontentsline{exercise}{figure}{Exercise 1}' \
            '\\phantomsection\\addcontentsline{exercise:1}{figure}{Exercise 1}' \
            '\\phantomsection\\addcontentsline{exercise:1_}{figure}{Exercise 1}'
    dest = json.loads(json.dumps(Span(['exercise:1', [], []], [RawInline('tex', latex), Str(u'Exercise'), Space(), Str(u'1')])))
    assert pandoc_listof.collect(src['t'], src['c'], 'latex', {}) == None
    assert json.loads(json.dumps(src)) == dest

