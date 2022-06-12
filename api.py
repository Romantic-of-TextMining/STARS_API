from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import domain.model as model
from adapters import orm
from adapters import repository
from service_layer import services
from service_layer.request import tf_idf_request
from domain import tf_idf, cos_sim, rank

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)

#@app.route("/")
#def index():
#    return "<h1>Hello!</h1>", 200

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


@app.route("/v1/textcloud/<string:field>", methods=["GET"])
def get_text_cloud(field):
    #args = tf_idf_request.TfIdfRequestHandler(field)
    msg = {}
    msg["field"] = field
    result = tf_idf.TfIdfCalculator.get_tf_idf(msg)
    return result

@app.route("/v1/cos_sim", methods=["GET"])
def get_cos_sim():
    msg = {}
    msg["field"] = request.args.get("field")
    msg["query"] = request.args.get("query")
    result = cos_sim.CosSimCalCulator.get_cos_sim_by_query(msg)
    return result

#@app.route("/v1/high_score", methods=["POST"])
#def high_score_endpoint():
#    print("In high_score_endpoint()\n")
#    session = get_session()

#    return {"ranking": ranking}, 201



'''
from domain import tf_idf
msg = {}
msg["field"] = "en_14_participation_in_public_policy"
result = tf_idf.TfIdfCalculator.get_tf_idf(msg)
'''