import os
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    files = [file for file in os.listdir() if os.path.isfile(file)]
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run(debug=True)