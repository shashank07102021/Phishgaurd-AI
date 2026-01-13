from flask import Blueprint, render_template

incidents_bp = Blueprint("incidents", __name__, url_prefix="/incidents")

@incidents_bp.route("/")
def incidents():
    return render_template("incidents.html")
