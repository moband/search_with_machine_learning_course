#
# A simple endpoint that can receive documents from an external source, mark them up and return them.  This can be useful
# for hooking in callback functions during indexing to do smarter things like classification
#
from flask import (
    Blueprint, request, abort, current_app, jsonify
)
import fasttext
import json
import nltk


bp = Blueprint('documents', __name__, url_prefix='/documents')

nltk.download('punkt')
    
# Take in a JSON document and return a JSON document
@bp.route('/annotate', methods=['POST'])
def annotate():
    if request.mimetype == 'application/json':
        the_doc = request.get_json()
        response = {}
        cat_model = current_app.config.get("cat_model", None) # see if we have a category model
        syns_model = current_app.config.get("syns_model", None) # see if we have a synonyms/analogies model
        # We have a map of fields to annotate.  Do POS, NER on each of them
        sku = the_doc["sku"]
        for item in the_doc:
            if item != "sku":
                the_text = the_doc[item]

                if syns_model and (item == 'name'):
                    name_synonyms = []
                    tokens = nltk.word_tokenize(the_text)
                    for token in tokens:
                        syns = syns_model.get_nearest_neighbors(token.strip().lower())
                        name_synonyms += [ syn for score, syn in syns if score > 0.9 ]
                    response['name_synonyms'] = list(set(name_synonyms))

        print(json.dumps(response, indent=2))

        return jsonify(response)
    abort(415)
