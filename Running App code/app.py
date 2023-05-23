from flask import Flask
from flask import request
from draw_map import get_map
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/safe_route")
def safe_route():
    source = request.args.get('source')
    destination = request.args.get('destination')
    get_map(source, destination)
    return render_template('routes.html')