__revision__ = '$Id: runtests.py,v 1.2 2003-10-15 14:57:00 alf Exp $'

from logilab.common.testlib import main

if __name__ == '__main__':
    import sys, os
    main(os.path.dirname(sys.argv[0]) or '.')
