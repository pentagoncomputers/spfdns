'''
Created on 1 Jul 2019

@author: dermot@pentagoncomputers.com
@copyright: Pentagon Computers Ltd, 2019.
'''
from database import get_db


def is_ok(ip, domain):
    domain = domain.rstrip('.')  # remove trailing dot if there is one
    cnx = get_db()
    try:
        cursor = cnx.cursor()

        # vw_spf is just a simple view with columns domain_name and ip_addr.  With an entry for
        # each ip address that should pass spf for domain name.
        cursor.execute("""select *
        FROM vw_spf
        WHERE domain_name = %s
        AND ip_addr = %s""", (domain, str(ip)))

        row = cursor.fetchone()
        if row is None or row[0] is None:
            return False

        print('Matched on row: ' + repr(row))
        return True
    finally:
        cnx.close()


def get_domains():
    cnx = get_db()
    try:
        cursor = cnx.cursor()

        cursor.execute("""select distinct(domain_name)
        FROM vw_spf""")

        results = []

        for row in cursor:
            results.append(row[0])

        return results
    finally:
        cnx.close()