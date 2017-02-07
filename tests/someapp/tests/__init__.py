from __future__ import print_function

from neomodel import db, change_neo4j_password, clear_neo4j_database
from neo4j.v1 import CypherError

# Travis default password dance
try:
    clear_neo4j_database(db)
except CypherError as ce:
    # handle instance without password being changed
    if 'The credentials you provided were valid, but must be changed before you can use this instance' in str(ce):
        change_neo4j_password(db, 'test')
        db.set_connection('bolt://neo4j:test@localhost:7687')

        print("New database with no password set, setting password to 'test'")
        print("Please 'export NEO4J_BOLT_URL=bolt://neo4j:test@localhost:7687' for subsequent test runs")
    else:
        raise ce
