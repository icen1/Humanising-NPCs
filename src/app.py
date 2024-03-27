from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)



@app.route("/")
def home():
    return redirect(url_for("environments_page"))

@app.route("/create_environment_page")
def create_environment_page():
    return render_template("create_environment.html")

@app.route("/environments_page")
def environments_page():
    return render_template("environments.html")

@app.route("/create_environment", methods=["POST"])
def create_environment():
    # Get the values from the form
    environment_name = request.form.get("environmentName")
    npc_base_traits = request.form.get("npcBaseTraits")
    npc_action = request.form.get("npcActions")
    # run code for actual parsing
    return redirect(url_for("create_environment_page"))

@app.route("/create_npc", methods=["POST"])
def create_npc():
    # get the slider value
    slider_value = request.form.get("sliderValue")
    # run code for actual parsing
    return redirect(url_for("environments_page"))
