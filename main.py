from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for, \
    send_file

import urllib.parse
import json 

from functools import wraps

from models.matrix import Matrix
from models.genetic import Genetic
from models.fileHandler import FileHandler

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
    return render_template("index.html", default_persons_per_group=3)


@app.route('/reader', methods=['POST', 'GET'])
@redirect_to_home_if_get
def process_file():
    file = request.files['file_to_upload']
    matrix = FileHandler.get_matrix_from_excel(file)
    matrix_class = Matrix(matrix)
    genetic_class = Genetic(matrix_class.individuals, int(request.form['persons_per_group']))
    genetic_class.calculate()
    groups = genetic_class.legible_groups(genetic_class.groups)

    return render_template(
        "results.html",
        genetic_class=genetic_class,
        matrix_class=genetic_class.matrix_class,
        groups=groups,
        parsed_groups=urllib.parse.quote(json.dumps(groups))
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
