import os
from flask import Flask, render_template, redirect, url_for, request, flash
import file_service
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
def index():
    files = [file for file in os.listdir(os.path.join(os.getcwd(), 'tests_file'))]
    return render_template('index.html', files=files)


@app.route('/delete/<name_file>', methods=['POST'])
def delete_file(name_file):
    name_file = os.path.join(os.getcwd(), 'tests_file', name_file)
    file_service.delete_file(name_file)

    return redirect (url_for('index'))


@app.route('/read_file/<name_file>')
def read_file(name_file):
    content = file_service.read_file(os.path.join(os.getcwd(), 'tests_file', name_file))
    return content


@app.route('/update/<name_file>', methods=['GET', 'POST'])
def update_file(name_file):
    if request.method == 'POST':
        content = request.form.get('content', '')
        with open(os.path.join(os.getcwd(), 'tests_file', name_file), 'w') as file:
            file.write(content)

        flash(f'File {name_file} was successfully updated', category='success')

        return redirect(url_for('index'))

    content = file_service.read_file(os.path.join(os.getcwd(), 'tests_file', name_file))

    return render_template('update_file.html', content=content)


if __name__ == '__main__':
    app.run(debug=True)