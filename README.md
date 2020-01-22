# Joo(mla)Bro(ken)L(ink)s - JooBroLs

## Description

There are a number of tools to search your site for broken links, including some nice
browser plugins that can colour your page.

Joomla (https://joomla.org) is a CMS that makes it easy to manage small to large websites.
Its routing mechanism is designed to give flexibility. But this flexibility sometimes
causes the router to not generate a 404 for incorrect links. Instead the result is an empty,
but valid page.

This little program was designed specifically to find those links. It works as most of the
other "broken link detectors", but also catches those links to "blank Joomla pages".

It's a command line program written in Python (3). You probably need a few non-standard
Python packages, but I've not listed those at this point.

## Usage

    ./joobrols.py <options> <url>

<options> are

    --help (-h)
    --verbose (-v)
    --max <n>

The last option allows you to maximize the number of pages analyzed, in case your want a
small dry-run before going the full monty.

## Miscellanea

The implementation is single threaded and reads every page synchronously. It could
probably be made a lot faster by putting each page scraping in a separate thread. Merge requests
are welcome, but it has enough speed for my purpose.
