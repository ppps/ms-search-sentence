#!/usr/bin/env python3
"""db_search

Usage:
    db_search [-]
    db_search [-j]
    db_search SENTENCE
"""

import json
import subprocess
import sys


from docopt import docopt
import psycopg2


def asrun(ascript):
    "Run the given AppleScript and return the standard output and error."

    osa = subprocess.Popen(['osascript', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
    result = osa.communicate(ascript.encode('utf-8'))[0].decode('utf8')
    if result[-1] == '\n':
        return result[:-1]
    else:
        return result


def asquote(astr):
    "Return the AppleScript equivalent of the given string."

    astr = astr.replace('"', '" & quote & "')
    return '"{}"'.format(astr)


def get_sentence():
    """Fetch search sentence from argv or stdin"""
    args = docopt(__doc__)
    if args['-']:
        sentence = sys.stdin.read()
    elif args['-j']:
        # Code units from javascript
        code_units = json.loads(sys.stdin.read())
        sentence = ''.join([chr(c) for c in code_units])
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
    if len(results) == 1:
        # Choose this result automatically
        title = results[0][1]
    else:
        # Prompt user to choose title
        result_dict = {row_to_string(row): row[1] for row in results}
        title = result_dict[choose_from_list(result_dict.keys())]
    print(title)
    # Do something with `title` here


if __name__ == '__main__':
    main()
