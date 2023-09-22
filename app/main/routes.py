from apiflask import APIBlueprint as Blueprint
from flask import current_app as app
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError


from app import db
from app.errors.handlers import error_response
from app.models import Table

from app.lib.ask import get_scope, get_summary

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return jsonify(hello="scaffold")

@bp.route("/scope", methods=['GET'])
def scope_of_work():

    args = request.args
    print("here", args.get("limit"))

    limit = args.get("limit")
    question = args.get("question")
    res = get_scope(question, limit)
    final_res = res["data"]["Get"]["Issue"][0]["_additional"]["generate"]["groupedResult"]
    return jsonify(response=final_res)

@bp.route("/task-summary", methods=['GET'])
def task_summary():

    args = request.args
    
    limit = args.get("limit")
    question = args.get("question")
    res = get_summary(question, limit)
    final_res = res["data"]["Get"]["Issue"][0]["_additional"]["generate"]["groupedResult"]
    return jsonify(response=final_res)

@bp.route("/log")
def log():
    app.logger.debug("This is a debug log, you can only see it when app.debug is True")
    app.logger.info("Some info")
    app.logger.warn("Warning")
    app.logger.error("Something was broken")
    return jsonify(log="ok")


@bp.route("/redis/<key>", methods=["GET"])
def get_redis_value(key):
    v = app.redis.get(key) or b""
    return jsonify(result=v.decode())


@bp.route("/redis/<key>/<value>", methods=["PUT"])
def set_redis_value(key, value):
    return jsonify(set=app.redis.set(key, value))


@bp.route("/db/<hash>", methods=["PUT"])
def set_hash(hash):
    t = Table(hash=hash)
    db.session.add(t)

    try:
        db.session.commit()
        result = True
    except IntegrityError as e:
        app.logger.error(e)
        result = False

    return jsonify(result=result)


@bp.route("/db/<int:id>", methods=["GET"])
def get_hash(id):
    t = Table.query.filter_by(id=id).scalar()
    return jsonify(hash=t.hash if t else "")


@bp.route("/error/<int:code>")
def error(code):
    app.logger.error(f"Error: {code}")
    return error_response(code)
