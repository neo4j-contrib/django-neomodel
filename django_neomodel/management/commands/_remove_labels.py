import re
import sys

from neomodel import drop_indexes, db

def drop_constraints(quiet=True, stdout=None):
    """
    Discover and drop all constraints.

    :type: bool
    :return: None
    """

    results, meta = db.cypher_query("CALL db.constraints()")
    pattern = re.compile(':(.*) \).*\.(\w*)')   # Pattern for matching label and property in query 
    for (constr_name, constr_query, _constr_obj) in results:
        db.cypher_query('DROP CONSTRAINT ' + constr_name)
        match = pattern.search(constr_query)
        stdout.write(''' - Droping unique constraint and index on label {0} with property {1}.\n'''.format(
            match.group(1), match.group(2)))
    stdout.write("\n")


def remove_all_labels(stdout=None):
    """
    Calls functions for dropping constraints and indexes.

    :param stdout: output stream
    :return: None
    """

    if not stdout:
        stdout = sys.stdout

    stdout.write("Droping constraints...\n")
    drop_constraints(quiet=False, stdout=stdout)

    stdout.write('Droping indexes...\n')
    drop_indexes(quiet=False, stdout=stdout)


def drop_indexes(quiet=True, stdout=None):
    """
    Discover and drop all indexes.

    :type: bool
    :return: None
    """

    results, meta = db.cypher_query("CALL db.indexes()")
    for index in results:
        idx_name = index[1]
        db.cypher_query('DROP INDEX ' + index[1])

        idx_label = index[7]
        idx_property = index[8]
        if not idx_property:
            if not idx_label:
                stdout.write(' - Dropping index without label and without property.\n')
            else:
                stdout.write(' - Dropping index on label {0} without property.\n'.format(
                    idx_label))
        else:
            stdout.write(' - Dropping index on label {0} with property {1}.\n'.format(
                idx_label, idx_property))
    stdout.write("\n")

