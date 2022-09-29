from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for, \
    send_file

import urllib.parse
import json 

from functools import wraps

from models.person import Person
from models.genetic import Genetic
from models.fileHandler import FileHandler
from models.config import Config

app = Flask(__name__)


def redirect_to_home_if_get(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'GET':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    config_model = Config()
    return render_template(
        "index.html",
        default_persons_per_group=config_model.get_config_value(['app', 'default_persons_per_group']),
        default_preference_columns=config_model.get_config_value(['app', 'default_preference_columns']),
    )


@app.route('/reader', methods=['POST', 'GET'])
@redirect_to_home_if_get
def process_file():
    file = request.files['file_to_upload']
    matrix = FileHandler.get_matrix_from_excel(file)
    person_class = Person(matrix=matrix, number_of_preferences=int(request.form['number_of_preferences']))
    genetic_class = Genetic(person_class, int(request.form['persons_per_group']))
    genetic_class.calculate()
    groups = genetic_class.legible_groups(genetic_class.groups)

    return render_template(
        "results.html",
        parsed_groups=urllib.parse.quote(json.dumps(groups)),
        genetic_class=genetic_class,
        person_class=genetic_class.person_class,
        groups=groups
    )


@app.route('/download', methods=['POST', 'GET'])
@redirect_to_home_if_get
def download_excel_file():
    form_data = request.form['parsed_groups']
    io = FileHandler.get_json_to_io_download(form_data)

    return send_file(io, 
        attachment_filename="tdd-excel.xlsx", 
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True
    )


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=5000)
