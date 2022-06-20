from flask import Flask, request

from domain import tf_idf, cos_sim, rank

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_route():
    result = {
        "description": "Welcome to STARS_API"
    }
    return result,200

@app.route("/v1/rank", methods=["GET"])
def get_rank():
    msg = {}
    msg["field"] = request.args.get("field")
    result = rank.RankCalCulator.get_rank_by_field(msg)
    return result

@app.route("/v1/textcloud", methods=["GET"])
def get_text_cloud():
    #args = tf_idf_request.TfIdfRequestHandler(field)
    msg = {}
    msg["field"] = request.args.get("field")
    result = tf_idf.TfIdfCalculator.get_tf_idf(msg)
    return result

@app.route("/v1/cos_sim", methods=["GET"])
def get_cos_sim():
    msg = {}
    msg["field"] = request.args.get("field")
    msg["query"] = request.args.get("query")
    result = cos_sim.CosSimCalCulator.get_cos_sim_by_query(msg)
    return result
