#!/usr/bin/env python

"""
Pandoc filter to create lists of all kinds
"""

from pandocfilters import toJSONFilters, walk, Str, Plain, Link, BulletList, Para, RawInline
from functools import reduce
import io
import sys
import codecs
import json
import re
import unicodedata

collections = {}

def stringify(x, format):
    """Walks the tree x and returns concatenated string content,
    leaving out all formatting.
    """
    result = []

    def go(key, val, format, meta):
        if key in ['Str', 'MetaString']:
            result.append(val)
        elif key == 'Code':
            result.append(val[1])
        elif key == 'Math':
            # Modified from the stringify function in the pandocfilter package
            if format == 'latex':
                result.append('$' + val[1] + '$')
            else:
                result.append(val[1])
        elif key == 'LineBreak':
            result.append(" ")
        elif key == 'Space':
            result.append(" ")

    walk(x, go, format, {})
    return ''.join(result)

def collect(key, value, format, meta):
    # Is it a link with a right tag?
    if key == 'Span':

        # Get the Span
        [[anchor, classes, other], text] = value

        # Is the anchor correct?
        result = re.match('^([a-zA-Z][\w.-]*):([\w.-]+)$', anchor)
        if result:
            global collections

            # Compute the name
            name = result.group(1)

            # Compute the identifier
            identifier = result.group(2)

            # Prepare the new collection if needed
            if name not in collections:
                collections[name] = []

            # Store the new item
            collections[name].append({'identifier': identifier, 'text': stringify(text, format)})

            # Special case for LaTeX output
            if format == 'latex':
                latex = '\\phantomsection\\addcontentsline{' + name + '}{figure}{' + stringify(text, format) + '}'
                text.insert(0, RawInline('tex', latex))
                value[1] = text

def listof(key, value, format, meta):
    # Is it a paragraph with only one string?
    if key == 'Para' and len(value) == 1 and value[0]['t'] == 'Str':

        # Is it {tag}?
        if re.match('^{[a-zA-Z][\w.-]*}$', value[0]['c']):

            # Get the collection name
            name = value[0]['c'][1:-1]

            # Is it an existing collection
            if name in collections:

                if format == 'latex':
                    # Special case for LaTeX output
                    if 'toccolor' in meta:
                        colorlink = '\\hypersetup{linkcolor=' + stringify(meta['toccolor']['c'], format) + '}'
                    else:
                        colorlink = '\\hypersetup{linkcolor=black}'
                    return Para([RawInline('tex', colorlink + '\\makeatletter\\@starttoc{' + name + '}\\makeatother')])

                else:
                    # Prepare the list
                    elements = []

                    # Loop on the collection
                    for value in collections[name]:

                        # Add an item to the list
                        try:
                            # pandoc 1.15
                            link = Link([Str(value['text'])],['#' + name + ':' + value['identifier'], ''])
                        except ValueError:
                            # pandoc 1.16
                            link = Link(['', [], []], [Str(value['text'])],['#' + name + ':' + value['identifier'], ''])

                        elements.append([Plain([link])])

                    # Return a bullet list
                    return BulletList(elements)

        # Special case where the paragraph start with '{{...'
        elif re.match('^{{[a-zA-Z][\w.-]*}$', value[0]['c']):
            value[0]['c'] = value[0]['c'][1:]

def main():
    toJSONFilters([collect, listof])

if __name__ == '__main__':
    main()

