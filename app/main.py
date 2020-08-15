from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", default_persons_per_group=3)


@app.route('/reader', methods=['POST', 'GET'])
def process_file():
    if request.method == 'GET':
        return redirect(url_for('home'))


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
