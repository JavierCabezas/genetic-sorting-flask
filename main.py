from flask import Flask, \
    Response, \
    render_template, \
    request, \
    redirect, \
    url_for, \
    send_file

from pyexcel_xlsx import get_data, \
    save_data

import urllib.parse
import json 

from io import BytesIO
from datetime import datetime
from functools import wraps
from collections import OrderedDict

from models.person import Person
from models.genetic import Genetic

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
    data = get_data(file)
    first_index = next(iter(data))
    matrix = data[first_index][1:]
    person_class = Person(matrix)
    genetic_class = Genetic(person_class, int(request.form['persons_per_group']))
    genetic_class.calculate()
    groups = genetic_class.legible_groups(genetic_class.groups)

    return render_template(
        "results.html",
        genetic_class=genetic_class,
        person_class=genetic_class.person_class,
        groups=groups,
        parsed_groups=urllib.parse.quote(json.dumps(groups))
    )


@app.route('/download', methods=['POST', 'GET'])
@redirect_to_home_if_get
def download_excel_file():
    form_data = request.form['parsed_groups']
    row_data = json.loads(urllib.parse.unquote(form_data))
    group_size = len(row_data[0]['rows'])
    number_of_groups = len(row_data)
    excel_matrix = [[0 for x in range(group_size+1)] for y in range(number_of_groups)]
    row_idx = 0

    for row in row_data:
        excel_matrix[row_idx][0] = "Group " + str(row_idx+1)
        person_idx = 0
        for person in row['rows']:
            excel_matrix[row_idx][person_idx+1] = person['name']
            person_idx = person_idx + 1
        row_idx = row_idx + 1

    
    data = OrderedDict()
    data.update({"Sheet 1": excel_matrix})
    io = BytesIO()
    save_data(io, data)
    io.seek(0)

    return send_file(io, 
        attachment_filename="tdd-excel.xlsx", 
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True
    )


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=5000)
