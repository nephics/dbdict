import dbdict
import sqlite3

#
# Perform some tests using the dbdict module
#

d = dbdict.dbdict(':memory:')

d[1] = 'test'
assert d[1] == 'test'

d[1] += '1'
assert d[1] == 'test1'

try:
    assert d[2], 'Lookup did not fail on non-existent key'
except KeyError:
    pass

# test len
assert len(d) == 1, 'Failed to count number of items'

# test clear
d.clear()
assert len(d) == 0, 'Database not cleared as expected'

# test with list of items as (key, value) pairs
range10 = list(range(10))
items = [(i, i) for i in range10]
d.update(items)
assert list(d.items()) == items, 'Failed to update using list'
d.clear()

# test with tuple of items as (key, value) pairs
d.update(tuple(items))
assert list(d.items()) == items, 'Failed to update using tuple'
d.clear()

# test with dict
d.update(dict(items))
assert list(d.items()) == items
d.clear()

# test with generator
d.update((i, i) for i in range10)
assert list(d.items()) == items, 'Failed to update using generator'

# check the std. dict methods
assert list(d.keys()) == range10
assert list(d.values()) == range10
assert list(d.items()) == items

# test get
assert d.get(range(8, 12)) == items[-2:]

# test remove
d.remove(range(8, 10))
assert len(d.get(range(8, 10))) == 0, 'Items not removed successfully'

d.clear()

# test with key,value pairs as parameters
d.update(foo=1, bar=2)
assert list(d.items()) == [('foo', 1), ('bar', 2)], \
    'keyword assignment not successful'

# test popitem
while True:
    try:
        value = d.popitem()
        assert value in [('foo', 1), ('bar', 2)], \
            'Popitem not in expected result set'
    except StopIteration:
        break

# test setdefault
d.setdefault(10, 10)
assert d[10] == 10, 'Failed to set default value'

# test vacuum call (no assert)
d.reindex()

# test vacuum call (no assert, and call has no effect on an in memory db)
d.vacuum()

# test close call (assert is given reading from closed database)
d.close()

# try reading from a closed database
try:
    d[1] = 1
    raise AssertionError('Database not closed')
except sqlite3.ProgrammingError:
    pass
