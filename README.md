You'll probably never need this
===============================

You might end up using 2 versions of Python, say 2.5 and 2.6. They 
coexist fairly well, but you might have a compiled version of MySQLdb
that works on 2.5 sitting in a (semi-)random directory, and one 
installed in 2.6's site-packages. Why this happens doesn't matter, 
but you're right--it's wrong. 

That's OK though, like I said, you'll probably never need this.

How to use (if you do need it)
---------------------------------

1. Copy `require.py` to your scripts directory
2. Create a config file `require-paths.conf` which looks like this:
    [global]
    path = /:-separated/list/of/paths/to/put/on/sys.path
    
    [2.5]
    multiprocessing = /path/to/where/multiprocessing/is/
    other = /path/to/where/other/thing/is/
3. Now you're ready to rock
    from require import require
    multiprocessing = require('multiprocessing')
    MySQLdb = require('MySQLdb')
    
    \# you can do "from" style too, but no wildcards!
    os, sep = require('os', names=['pathsep'])

Read the source to find out more tricks of the trade
