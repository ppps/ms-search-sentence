#!/usr/bin/env python3
"""db_search

Usage:
    db_search [-]
    db_search SENTENCE
"""

import subprocess
import sys


from docopt import docopt
import psycopg2


def asrun(ascript):
    "Run the given AppleScript and return the standard output and error."

    osa = subprocess.Popen(['osascript', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
    return osa.communicate(ascript.encode('utf-8'))[0].decode('utf8')


def asquote(astr):
    "Return the AppleScript equivalent of the given string."

    astr = astr.replace('"', '" & quote & "')
    return '"{}"'.format(astr)


def get_sentence():
    """Fetch search sentence from argv or stdin"""
    args = docopt(__doc__)
    if args['-']:
        sentence = sys.stdin.read()
    else:
        sentence = args['SENTENCE']
    return sentence


def search_for_sentence(sentence):
    """Return date and title of the matches for sentence in the database"""

    search_query = '''\
      select date, title
        from "20171210".articles a
       where content_tsvector @@ phraseto_tsquery('english', %(phrase)s)
         and a.date < '2017-11-30'
         and a.date > '2017-08-20'
    order by a.date desc;
    ;
    '''
    with psycopg2.connect('dbname=morningstaronline user=admin') as conn:
        cur = conn.cursor()
        sql_args = dict(phrase=sentence)
        cur.execute(search_query, sql_args)
        results = cur.fetchall()
    return results


def choose_from_list(string_list):
    """Prompt the user to choose and string from several and return it"""
    ascript = '''\
tell the current application
	choose from list {{ {str_list} }}
end tell
'''
    quoted_strings = ', '.join([asquote(s) for s in string_list])
    return asrun(ascript.format(str_list=quoted_strings))


def row_to_string(row):
    """Format a tuple of (date, title) fetched from the database"""
    date, title = row
    return f'{date:%Y-%m-%d}: {title}'


def main():
    sentence = get_sentence()
    results = search_for_sentence(sentence)


if __name__ == '__main__':
    main()
