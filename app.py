import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
type_to_imagesrc = {
    "physical": "/static/images/physicaltitle3.png",
    "digital": "/static/images/digitaltitle.png",
    "experiential": "/static/images/experientialtitle.png",
    "all": "/static/images/physicaltitle2.png"
}

Session(app)



@app.context_processor
def utility_processor():
    def round_num(value, precision):
        return round(value, precision)

    return dict(round_num=round_num)


@app.context_processor
def utility_processor():
    def format_num(value):
        return "{:,.2f}".format(value)

    return dict(format_num=format_num)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/projects/<project_type>")
def projects(project_type):
    imagesrc = type_to_imagesrc.get(project_type, "")
    return render_template("projects.html", tags=project_type,imagesrc=imagesrc)

