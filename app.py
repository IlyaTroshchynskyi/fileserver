import os
from flask import Flask, render_template, redirect, url_for
import file_service
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
def index():
    files = [file for file in os.listdir() if os.path.isfile(file)]
    return render_template('index.html', files=files)


@app.route('/delete/path_file')
def delete_file(path_file):

    file_service.delete_file(path_file)

    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)