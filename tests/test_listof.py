# This Python file uses the following encoding: utf-8    
from unittest import TestCase
from pandocfilters import Span, Str, Space, Para, BulletList, Plain, Link, RawInline, Header

import json
import pandoc_listof

def init():
    pandoc_listof.collections = {}
    pandoc_listof.headers = [0, 0, 0, 0, 0, 0]

def createLink(attributes, text, reference_title):
    if pandoc_listof.pandoc_version() < '1.16':
        return Link(text, reference_title)
    else:
        return Link(attributes, text, reference_title)

def test_simple():
    init()

    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Span(['exercise:2', [], []], [Str(u'Exercise'), Space(), Str(u'2')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Para([Str(u'{exercise}')])))
    dest = json.loads(json.dumps(BulletList([
        [Plain([createLink(['', [], []], [Str(u'Exercise 1')], ['#exercise:1', ''])])],
        [Plain([createLink(['', [], []], [Str(u'Exercise 2')], ['#exercise:2', ''])])]
    ])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], '', {}))) == dest

def test_latex():
    init()

    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    pandoc_listof.collect(src['t'], src['c'], 'latex', {})

    src = json.loads(json.dumps(Span(['exercise:2', [], []], [Str(u'Exercise'), Space(), Str(u'2')])))
    pandoc_listof.collect(src['t'], src['c'], 'latex', {})

    src = json.loads(json.dumps(Para([Str(u'{exercise}')])))
    dest = json.loads(json.dumps(Para([RawInline(
        'tex',
        '\\hypersetup{linkcolor=black}\\makeatletter\\@starttoc{exercise}\\makeatother'
    )])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], 'latex', {}))) == dest

def test_toccolor():
    init()

    meta = {'toccolor': {'t': 'MetaInlines', 'c': [{'t': 'Str', 'c': 'red'}]}}
    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    pandoc_listof.collect(src['t'], src['c'], 'latex', meta)

    src = json.loads(json.dumps(Span(['exercise:2', [], []], [Str(u'Exercise'), Space(), Str(u'2')])))
    pandoc_listof.collect(src['t'], src['c'], 'latex', meta)

    src = json.loads(json.dumps(Para([Str(u'{exercise}')])))
    dest = json.loads(json.dumps(Para([RawInline(
        'tex',
        '\\hypersetup{linkcolor=red}\\makeatletter\\@starttoc{exercise}\\makeatother'
    )])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], 'latex', meta))) == dest

def test_double_curly_bracket():
    init()

    src = json.loads(json.dumps(Para([Str(u'{{exercise}')])))
    dest = json.loads(json.dumps(Para([Str(u'{exercise}')])))

    pandoc_listof.listof(src['t'], src['c'], '', {})

    assert src == dest

def test_with_number():
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

    src = json.loads(json.dumps(Para([Str(u'{exercise}')])))
    dest = json.loads(json.dumps(BulletList([
        [Plain([createLink(['', [], []], [Str(u'Exercise 1')], ['#exercise:1', ''])])],
        [Plain([createLink(['', [], []], [Str(u'Exercise 2')], ['#exercise:2', ''])])],
        [Plain([createLink(['', [], []], [Str(u'Exercise 3')], ['#exercise:3', ''])])],
        [Plain([createLink(['', [], []], [Str(u'Exercise 4')], ['#exercise:4', ''])])],
    ])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], '', {}))) == dest

    src = json.loads(json.dumps(Para([Str(u'{exercise:1}')])))
    dest = json.loads(json.dumps(BulletList([
        [Plain([createLink(['', [], []], [Str(u'Exercise 1')], ['#exercise:1', ''])])],
        [Plain([createLink(['', [], []], [Str(u'Exercise 2')], ['#exercise:2', ''])])],
    ])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], '', {}))) == dest

    src = json.loads(json.dumps(Para([Str(u'{exercise:2}')])))
    dest = json.loads(json.dumps(BulletList([
        [Plain([createLink(['', [], []], [Str(u'Exercise 3')], ['#exercise:3', ''])])],
        [Plain([createLink(['', [], []], [Str(u'Exercise 4')], ['#exercise:4', ''])])],
    ])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], '', {}))) == dest

def test_with_number_latex():
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

    src = json.loads(json.dumps(Para([Str(u'{exercise}')])))
    dest = json.loads(json.dumps(Para([RawInline(
        'tex',
        '\\hypersetup{linkcolor=black}\\makeatletter\\@starttoc{exercise}\\makeatother'
    )])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], 'latex', {}))) == dest

    src = json.loads(json.dumps(Para([Str(u'{exercise:1}')])))
    dest = json.loads(json.dumps(Para([RawInline(
        'tex',
        '\\hypersetup{linkcolor=black}\\makeatletter\\@starttoc{exercise:1}\\makeatother'
    )])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], 'latex', {}))) == dest

def test_sharp():
    init()

    src = Header(1, [u'first-chapter', [], []], [Str(u'First'), Space(), Str('chapter')])
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Span(['exercise:1', [], []], [Str(u'Exercise'), Space(), Str(u'1')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})
    src = json.loads(json.dumps(Span(['exercise:2', [], []], [Str(u'Exercise'), Space(), Str(u'2')])))
    pandoc_listof.collect(src['t'], src['c'], '', {})

    src = Header(1, [u'first-chapter', [], []], [Str(u'First'), Space(), Str('chapter')])
    pandoc_listof.listof(src['t'], src['c'], '', {})

    src = json.loads(json.dumps(Para([Str(u'{exercise:#}')])))
    dest = json.loads(json.dumps(Para([RawInline(
        'tex',
        '\\hypersetup{linkcolor=black}\\makeatletter\\@starttoc{exercise:1_}\\makeatother'
    )])))

    assert json.loads(json.dumps(pandoc_listof.listof(src['t'], src['c'], 'latex', {}))) == dest

