from flask import Flask, request

import db_search as search

app = Flask(__name__)

@app.route('/lookup', methods=['POST'])
def lookup():
    code_units = request.form['codeunits']
    sentence = search.parse_code_units_json(code_units)
    joined_details = search.main(sentence)
    return joined_details
