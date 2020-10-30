"""A dictionary-like object with SQLite backend

This is a fork from the original version available at:
http://sebsauvage.net/python/snyppets/index.html#dbdict
"""

__version__ = '2.0'

import sqlite3
from collections.abc import MutableMapping
from os import path


class DbDict(MutableMapping):
    """DbDict, a dictionary-like object with SQLite back-end
    """
    def __init__(self, filename):
        if filename == ':memory:' or not path.isfile(filename):
            self.con = sqlite3.connect(filename)
            self._create_table()
        else:
            self.con = sqlite3.connect(filename)

    def _create_table(self):
        """Creates an SQLite table 'data' with the columns 'key' and 'value'
        where column 'key' is the table's primary key.

        Note: SQLite automatically creates an unique index for the 'key'
        column. The index may get fragmented with lots of
        insertions/updates/deletions therefore it is recommended to use
        reindex() when searches becomes gradually slower.
        """
        self.con.execute('create table data (key PRIMARY KEY,value)')
        self.con.commit()

    def __getitem__(self, key):
        """Return value for specified key"""
        row = self.con.execute('select value from data where key=?',
                               (key, )).fetchone()
        if not row:
            raise KeyError
        return row[0]

    def __setitem__(self, key, value):
        """Set value at specified key"""
        self.con.execute('insert or replace into data (key, value) '
                         'values (?,?)', (key, value))
        self.con.commit()

    def __delitem__(self, key):
        """Delete item (key-value pair) at specified key"""
        if key in self:
            self.con.execute('delete from data where key=?', (key, ))
            self.con.commit()
        else:
            raise KeyError

    def __iter__(self):
        """Return iterator over keys"""
        return self._iterquery(self.con.execute('select key from data'),
                               single_value=True)

    def __len__(self):
        """Return the number of stored items"""
        cursor = self.con.execute('select count() from data')
        return cursor.fetchone()[0]

    @staticmethod
    def _iterquery(cursor, single_value=False):
        """Return iterator over query result with pre-fetching of items in
        set sizes determined by SQLite backend
        """
        rows = True
        while rows:
            rows = cursor.fetchmany()
            for row in rows:
                if single_value:
                    yield row[0]
                else:
                    yield row

    def keys(self):
        """Return iterator of all keys in the database"""
        return self.__iter__()

    def values(self):
        """Return iterator of all values in the database"""
        return self._iterquery(self.con.execute('select value from data'),
                               single_value=True)

    def items(self):
        """Return iterator of all key-value pairs in the database"""
        return self._iterquery(self.con.execute('select key, value from data'))

    def clear(self):
        """Clear the database for all key-value pairs, and free up unsused
        disk space.
        """
        self.con.execute('drop table data')
        self.vacuum()
        self._create_table()

    def _update(self, items):
        """Perform the SQL query of updating items (list of key-value pairs)"""
        self.con.executemany('insert or replace into data (key, value)'
                             ' values (?, ?)', items)
        self.con.commit()

    def update(self, items=None, **kwds):
        """Updates key-value pairs in the database.

        Items (key-value pairs) may be given by keyword assignments or using
        the parameter 'items' a dict or list/tuple of items.
        """
        if isinstance(items, dict):
            self._update(items.items())
        elif isinstance(items, list) or isinstance(items, tuple):
            self._update(items)
        elif items:
            # probably a generator
            try:
                self._update(list(items))
            except TypeError:
                raise ValueError('Could not interpret value of parameter '
                                 '`items` as a dict, list/tuple or iterator.')

        if kwds:
            self._update(kwds.items())

    def popitem(self):
        """Pop a key-value pair from the database. Returns the next key-value
        pair which is then removed from the database."""
        res = self.con.execute('select key, value from data').fetchone()
        if res:
            key, value = res
        else:
            raise StopIteration
        del self[key]
        return key, value

    def close(self):
        """Close database connection"""
        self.con.close()

    def vacuum(self):
        """Free unused disk space from the database file.

        The operation has no effect if database is in memory.

        Note: The operation can take some time to run (around a half second per
        megabyte on the Linux box where SQLite is developed) and it can use up
        to twice as much temporary disk space as the original file while it is
        running.
        """
        self.con.execute('vacuum')
        self.con.commit()

    def get(self, keys):
        """Get item(s) for the specified key or list of keys.

        Items will be returned only for those keys that are defined. The
        function will pass silently (i.e. not raise an error) if one or more of
        the keys is not defined."""
        try:
            keys = tuple(keys)
        except TypeError:
            # probably a single key (ie not an iterable)
            keys = (keys,)
        return self.con.execute('select key, value from data where key in '
                                '%s' % (keys,)).fetchall()

    def remove(self, keys):
        """Removes item(s) for the specified key or list of keys.

        The function will pass silently (i.e. not raise an error) if one or
        more of the keys is not defined."""
        try:
            keys = tuple(keys)
        except TypeError:
            # probably a single key (ie not an iterable)
            keys = (keys,)
        self.con.execute('delete from data where key in %s' % (keys,))
        self.con.commit()

    def reindex(self):
        """Delete and recreate key index.

        Use this function if key lookup time becomes slower. This may happen as
        the index will become fragmented with lots of
        insertions/updates/deletions."""
        self.con.execute('reindex sqlite_autoindex_data_1')
        self.con.commit()


def dbdict(filename=':memory:'):
    """Open a persistent dictionary for reading and writing.

    The filename parameter is the base filename for the underlying database.
    When filename is ':memory:' (default value) the database is created in
    memory.
    """
    return DbDict(filename)
