from flask import (
    Flask,
    render_template,
    request,
    jsonify
)


from services.location_service import (
    find_location
)


from services.groundwater_service import (
    get_groundwater
)


from services.authority_service import (
    get_authority
)


from services.general_ai_service import (
    ask_general_ai
)


from services.rag_ai_service import (
    ask_rag
)


# ------------------------------------------------------------
# CREATE FLASK APPLICATION
# ------------------------------------------------------------

app = Flask(__name__)


# ------------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ------------------------------------------------------------
# AREA ANALYSIS
# ------------------------------------------------------------

@app.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze():

    data = request.get_json()


    location = data.get(
        "location",
        ""
    )


    issue = data.get(
        "issue",
        "groundwater"
    )


    if not location:

        return jsonify(
            {
                "error":
                "Please enter a location."
            }
        ), 400


    # Find Chennai locality
    location_info = find_location(
        location
    )


    # Get groundwater information
    groundwater = get_groundwater(
        location
    )


    # Get responsible authority
    authority = get_authority(
        issue
    )


    return jsonify(

        {
            "location":
            location_info,

            "groundwater":
            groundwater,

            "authority":
            authority
        }

    )


# ------------------------------------------------------------
# ASK AQUAGUARD
# ------------------------------------------------------------

@app.route(
    "/api/rag-chat",
    methods=["POST"]
)
def rag_chat():

    data = request.get_json()


    question = data.get(
        "question",
        ""
    )


    if not question:

        return jsonify(
            {
                "error":
                "Question is required."
            }
        ), 400


    result = ask_rag(
        question
    )


    return jsonify(
        result
    )


# ------------------------------------------------------------
# ASK GENERAL QUESTION
# ------------------------------------------------------------

@app.route(
    "/api/general-chat",
    methods=["POST"]
)
def general_chat():

    data = request.get_json()


    question = data.get(
        "question",
        ""
    )


    history = data.get(
        "history",
        []
    )


    if not question:

        return jsonify(
            {
                "error":
                "Question is required."
            }
        ), 400


    answer = ask_general_ai(

        question,

        history

    )


    return jsonify(

        {
            "answer":
            answer
        }

    )


# ------------------------------------------------------------
# FOLLOW-UP QUESTIONS
# ------------------------------------------------------------

@app.route(
    "/api/follow-up",
    methods=["POST"]
)
def follow_up():

    data = request.get_json()


    question = data.get(
        "question",
        ""
    )


    if not question:

        return jsonify(
            {
                "error":
                "Question is required."
            }
        ), 400


    result = ask_rag(
        question
    )


    return jsonify(
        result
    )


# ------------------------------------------------------------
# RUN APPLICATION
# ------------------------------------------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )