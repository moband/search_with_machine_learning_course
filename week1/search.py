#
# The main search hooks for the Search Flask application.
#
from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from week1.opensearch import get_opensearch

bp = Blueprint('search', __name__, url_prefix='/search')


# Process the filters requested by the user and return a tuple that is appropriate for use in: the query, URLs displaying the filter and the display of the applied filters
# filters -- convert the URL GET structure into an OpenSearch filter query
# display_filters -- return an array of filters that are applied that is appropriate for display
# applied_filters -- return a String that is appropriate for inclusion in a URL as part of a query string.  This is basically the same as the input query string
def process_filters(filters_input):
    # Filters look like: &filter.name=regularPrice&regularPrice.key={{ agg.key }}&regularPrice.from={{ agg.from }}&regularPrice.to={{ agg.to }}
    filters = []
    display_filters = []  # Also create the text we will use to display the filters that are applied
    applied_filters = ""
    for filter in filters_input:
        type = request.args.get(filter + ".type")
        display_name = request.args.get(filter + ".displayName", filter)
        key = request.args.get(filter + ".key")
        #
        # We need to capture and return what filters are already applied so they can be automatically added to any existing links we display in aggregations.jinja2
        applied_filters += "&filter.name={}&{}.type={}&{}.displayName={}".format(filter, filter, type, filter,
                                                                                 display_name)
        display_filters.append(display_name)
                                                                             
        #TODO: IMPLEMENT AND SET filters, display_filters and applied_filters.
        # filters get used in create_query below.  display_filters gets used by display_filters.jinja2 and applied_filters gets used by aggregations.jinja2 (and any other links that would execute a search.)
        if type == "range":
            range_from = request.args.get(filter + ".from")
            range_to = request.args.get(filter + ".to")
            applied_filters+="&{}.key={}&{}.from={}&{}.to={}".format(filter,key,filter,range_from,filter,range_to)
            range_filter={"range": { "regularPrice": { "gte": range_from } }}
            if range_to:
                range_filter['range']['regularPrice']['lt'] = range_to
            filters+=[range_filter]
            
        elif type == "terms":
            applied_filters+="&{}.key={}".format(filter,key)
            filters += [{"term": { "department": key }}]

    print("Filters: {}".format(filters))

    return filters, display_filters, applied_filters


# Our main query route.  Accepts POST (via the Search box) and GETs via the clicks on aggregations/facets
@bp.route('/query', methods=['GET', 'POST'])
def query():
    opensearch = get_opensearch() # Load up our OpenSearch client from the opensearch.py file.
    # Put in your code to query opensearch.  Set error as appropriate.
    error = None
    user_query = None
    query_obj = None
    display_filters = None
    applied_filters = ""
    filters = []
    sort = "_score"
    sortDir = "desc"
    if request.method == 'POST':  # a query has been submitted
        user_query = request.form['query']
        if not user_query:
            user_query = "*"
        sort = request.form["sort"]
        if not sort:
            sort = "_score"
        sortDir = request.form["sortDir"]
        if not sortDir:
            sortDir = "desc"
        query_obj = create_query(user_query, [], sort, sortDir)
    elif request.method == 'GET':  # Handle the case where there is no query or just loading the page
        user_query = request.args.get("query", "*")
        filters_input = request.args.getlist("filter.name")
        sort = request.args.get("sort", sort)
        sortDir = request.args.get("sortDir", sortDir)
        if filters_input:
            (filters, display_filters, applied_filters) = process_filters(filters_input)

        query_obj = create_query(user_query, filters, sort, sortDir)
    else:
        query_obj = create_query("*", [], sort, sortDir)

    print("query obj: {}".format(query_obj))
    response = opensearch.search(query_obj)   # TODO: Replace me with an appropriate call to OpenSearch
    
    # Postprocess results here if you so desire

    # print(response)
    if error is None:
        return render_template("search_results.jinja2", query=user_query, search_response=response,
                               display_filters=display_filters, applied_filters=applied_filters,
                               sort=sort, sortDir=sortDir)
    else:
        redirect(url_for("index"))


def create_query(user_query, filters, sort="_score", sortDir="desc"):
    print("Query: {} Filters: {} Sort: {}".format(user_query, filters, sort))

    fscore_query = {
                "function_score": {
                    "boost_mode": "multiply",
                    "functions": [
                    {
                        "field_value_factor": {
                        "factor": 3,
                        "field": "bestSellingRank",
                        "missing": 10000000,
                        "modifier": "reciprocal"
                        }
                    },
                    
                    {
                        "field_value_factor": {
                        "factor": 3.5,
                        "field": "customerReviewCount",
                        "missing": 1,
                        "modifier": "square"
                        }
                    }
                    ],
                    "query": {
                    "multi_match": {
                        "fields": [
                        "name^1000",
                        "shortDescription^10",
                        "longDescription^1"
                        ],
                        "query": user_query,
                        "type": "cross_fields"
                    }
                    },
                    "score_mode": "multiply"
                }
        }
    bool_query =  {"bool": {"must": [ fscore_query ],'filter':filters}}
    aggs = {
                "departments": {
                    "terms": {
                    "field": "department",
                    "missing": "N/A"
                    }
                },
                "missing_images": {
                    "missing": {
                    "field": "image"
                    }
                },
                "regularPrice": {
                    "range": {
                    "field": "regularPrice",
                    "ranges": [
                        {
                        "from": 0,
                        "key": "$",
                        "to": 100
                        },
                        {
                        "from": 100,
                        "key": "$$",
                        "to": 200
                        },
                        {
                        "from": 200,
                        "key": "$$$",
                        "to": 300
                        },
                        {
                        "from": 300,
                        "key": "$$$$",
                        "to": 400
                        },
                        {
                        "from": 500,
                        "key": "$$$$$"
                        }
                    ]}
                }
            }
   
    query_obj = {
        'size': 10,
        "query": bool_query,
        "aggs": aggs
    }

    
    return query_obj
