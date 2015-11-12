# pandoc-listof

*pandoc-listof* is a [pandoc] filter for listof all kinds of things.

Each paragraph containing only a string `{`*name*`}` will be replaced by a list of link pointing to all `span` whose `id`
is *name*`:`*identifier*.

Demonstration: Using [pandoc-listof-sample.md] as input gives output files in [pdf], [tex], [html], [epub], [md] and
other formats.

~~~
$ cat pandoc-listof-sample.md
% Sample use of automatic creation of lists
% Ch. Demko <chdemko@gmail.com>
% 04/11/2015

This is the first section
=========================

<span id="exercise:1">**Exercise 1**</span>

This is the first exercise.

<span id="theorem:1">**Theorem 1**</span>

This is the first theorem.

<span id="exercise:2">**Exercise 2**</span>

This is the second exercise.

This is the second section
==========================

<span id="exercise:3">**Exercise 3**</span>

This is the third exercise.

<span id="theorem:2">**Theorem 2**</span>

This is the second theorem.

List of exercices
=================

{exercise}

List of theorems
================

{theorem}

Unchanged
=========

{{theorem}
~~~

Converting the `pandoc-listof-sample.md` file will give:

~~~
This is the first section
=========================

<span id="exercise:1">**Exercise 1**</span>

This is the first exercise.

<span id="theorem:1">**Theorem 1**</span>

This is the first theorem.

<span id="exercise:2">**Exercise 2**</span>

This is the second exercise.

This is the second section
==========================

<span id="exercise:3">**Exercise 3**</span>

This is the third exercise.

<span id="theorem:2">**Theorem 2**</span>

This is the second theorem.

List of exercices
=================

-   [Exercise 1](#exercise:1)
-   [Exercise 2](#exercise:2)
-   [Exercise 3](#exercise:3)

List of theorems
================

-   [Theorem 1](#theorem:1)
-   [Theorem 2](#theorem:2)

Unchanged
=========

{theorem}
~~~

This filter can be combined with [`pandoc-numbering`](https://github.com/chdemko/pandoc-numbering):

~~~
$ cat pandoc-numbering-listof-sample.md
% Sample use of automatic creation of lists
% Ch. Demko <chdemko@gmail.com>
% 04/11/2015

This is the first section
=========================

Exercise #

This is the first exercise.

Theorem #

This is the first theorem.

Exercise #

This is the second exercise.

This is the second section
==========================

Exercise #

This is the third exercise.

Theorem #

This is the second theorem.

List of exercices
=================

{exercise}

List of theorems
================

{theorem}

Unchanged
=========

{{theorem}

Exercise ##
~~~

Converting the `pandoc-listof-sample.md` file will give:

~~~
$ pandoc --filter pandoc-numbering --filter pandoc-listof pandoc-numbering-listof-sample.md -t markdown
This is the first section
=========================

<span id="exercise:1">**Exercise 1**</span>

This is the first exercise.

<span id="theorem:1">**Theorem 1**</span>

This is the first theorem.

<span id="exercise:2">**Exercise 2**</span>

This is the second exercise.

This is the second section
==========================

<span id="exercise:3">**Exercise 3**</span>

This is the third exercise.

<span id="theorem:2">**Theorem 2**</span>

This is the second theorem.

List of exercices
=================

-   [Exercise 1](#exercise:1)
-   [Exercise 2](#exercise:2)
-   [Exercise 3](#exercise:3)

List of theorems
================

-   [Theorem 1](#theorem:1)
-   [Theorem 2](#theorem:2)

Unchanged
=========

{theorem}

Exercise \#
~~~

This version of pandoc-listof was tested using pandoc 1.15.1 and is known to work under linux, Mac OS X and Windows.

[pandoc]: http://pandoc.org/
[pandoc-listof-sample.md]: https://raw.githubusercontent.com/chdemko/pandoc-listof/master/pandoc-listof-sample.md

Usage
-----

To apply the filter, use the following option with pandoc:

    --filter pandoc-listof

Installation
------------

pandoc-listof requires [python], a programming language that comes pre-installed on linux and Mac OS X, and which is easily installed [on Windows].  Either python 2.7 or 3.x will do.

Install pandoc-listof as root using the bash command

    pip install pandoc-listof 

To upgrade to the most recent release, use

    pip install --upgrade pandoc-listof 

Pip is a script that downloads and installs modules from the Python Package Index, [PyPI].  It should come installed with your python distribution.  If you are running linux, pip may be bundled separately.  On a Debian-based system (including Ubuntu), you can install it as root using

    apt-get update
    apt-get install python-pip

[python]: https://www.python.org/
[on Windows]: https://www.python.org/downloads/windows/
[PyPI]: https://pypi.python.org/pypi


Getting Help
------------

If you have any difficulties with pandoc-listof, please feel welcome to [file an issue] on github so that we can help.

[file an issue]: https://github.com/chdemko/pandoc-listof/issues
