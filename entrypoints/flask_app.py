from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import domain.model as model
from adapters import orm
from adapters import repository
from service_layer import services
from service_layer.request import tf_idf_request
from domain import tf_idf


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)

#@app.route("/")
#def index():
#    return "<h1>Hello!</h1>", 200

@app.route("/v1/textcloud/<string:field>", methods=["GET"])
def text_cloud(field):
    #args = tf_idf_request.TfIdfRequestHandler(field)
    result = tf_idf.TfIdfCalculator.get_tf_idf(field)
    return result
#get para
#call tf-idf based on para


#@app.route("/v1/high_score", methods=["POST"])
#def high_score_endpoint():
#    print("In high_score_endpoint()\n")
#    session = get_session()

#    return {"ranking": ranking}, 201

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    print("In allocate_endpoint()\n")
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201
