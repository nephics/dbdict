A dictionary-like object with SQLite backend
============================================

Python dictionaries are very efficient objects for fast data access. But when
data is too large to fit in memory, you want to keep data on disk but available
for fast random access.

Here's a dictionary-like object which uses a SQLite database backend for random
access to the dictionary's key-value pairs:

  - You can work on datasets which do not fit in memory. Size is not limited by
    memory, but by disk. Can hold up to several tera-bytes of data (thanks to
    SQLite).

  - Behaves like a dictionary (can be used in place of a dictionary
    object in many cases) for storing numbers, strings and binary data.

  - Data persists between program runs, and is written to disk immediately
    when inserting a key-value pair in the dictionary.

  - ACID (data integrity): Storage file integrity is assured. No half-written
    data. It's really hard to mess up data.

  - Efficient: You do not have to re-write a whole database file when changing
    only one item. Only the relevant parts of the file are changed.

  - You can mix several key types (you can do d['foo']=bar and d[7]=5468) as
    with a regular dict object.

  - You can share this dictionary with other languages and systems (SQLite
    databases are portable, and the SQlite library is available on a wide range
    of systems/languages, from mainframes to PDA/iPhone, from Python to
    Java, C/C++, C#, Perl etc.)


Install using pip:

    python3 -m pip install https://github.com/nephics/dbdict/archive/main.zip

Use it like a standard dictionary, except that you give it a name
(eg.'tempdict'):

    from dbdict import dbdict
    d = dbdict('tempdict')
    d['foo'] = 'bar'
    # At this point, the key value pair foo and bar is written to disk.
    d['John'] = 'doh!'
    d['pi'] = 3.999
    d['pi'] = 3.14159  # replaces the previous version of pi
    d['pi'] += 1
    d.close()    # close the database file

You can access your dictionary later on:

    d = dbdict('tempdict')
    del d['foo']

    if 'John' in d:
        print 'John is in there !'
    print d.items()

For efficient inserting/updating a list of key-value pairs, use the update()
method:

    d.update([('f1', 'test'), ('f2', 'example')])
    d.update({'f1':'test', 'f2':'example'})
    d.update(f1='test', f2='example')

Use get() method to most efficiently get a number of items as specified by a
lis of keys:

    d.get(['f1', 'f2'])

Use remove() method to most efficiently remove a number of items as specified
by a list of keys:

    d.remove(['f1', 'f2'])

Create a memory-based (ie not filed based) SQLite database by the call:

    dbdict(':memory:')

Other special functionality as compared to dict:

    d.clear()    Clear all items (and free up unused disk space)
    d.reindex()  Delete and recreate the key index
    d.vacuum()   Free up unused disk space
    d.con        Access to the underlying SQLite connection (for advanced use)

Some things to note:

  - You can't directly store Python objects. Only numbers, strings and binary
    data. Objects need to be serialized first in order to be stored. Use e.g.
    pickle, json (or simplejson) or yaml for that purpose.

  - Explicit database connection closing using the close() method is not
    required. Changes are written on key-value assignment to the dictionary.
    The file stays open until the object is destroyed or the close() method is
    called.

    
This Python 3 compatible implementation is a fork from Seb Sauvage's original version of "dbdict", licensed CC BY 2.5., source available at: [http://sebsauvage.net/python/snyppets/index.html#dbdict]()

This implementation is licensed [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
