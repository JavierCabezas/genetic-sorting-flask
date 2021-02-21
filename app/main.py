from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for
from pyexcel_xlsx import get_data

from models.person import Person
from models.genetic import Genetic

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", default_persons_per_group=3)


@app.route('/reader', methods=['POST', 'GET'])
def process_file():
    if request.method == 'GET':
        return redirect(url_for('home'))
    else:
        file = request.files['file_to_upload']
        data = get_data(file)
        first_index = next(iter(data))
        matrix = data[first_index][1:]
        person_class = Person(matrix)
        genetic_class = Genetic(person_class, 3)
        genetic_class.calculate()


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
