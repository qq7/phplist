#!/usr/bin/python
"""Set PHPlist admin password, email and domain

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com
"""

import re
import sys
import getopt

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    email = ""
    domain = ""
    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "PHPlist Password",
            "Enter new password for the PHPlist 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "PHPlist Email",
            "Enter email address for the PHPlist 'admin' account.",
            "admin@example.com")

    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "PHPlist Domain",
            "Enter the domain to serve PHPlist.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    m = MySQL()
    m.execute('UPDATE phplist.phplist_admin SET password=\"%s\" WHERE loginname=\"admin\";' % password)
    m.execute('UPDATE phplist.phplist_admin SET email=\"%s\" WHERE loginname=\"admin\";' % email)
    m.execute('UPDATE phplist.phplist_config SET value=\"%s\" WHERE item=\"website\";' % domain)

if __name__ == "__main__":
    main()

