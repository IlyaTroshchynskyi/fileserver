import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
import file_service
from config import Configuration
from werkzeug.utils import secure_filename


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
    print(name_file)
    path = os.path.join(os.getcwd(), 'tests_file', name_file)
    print(path)
    extension = os.path.splitext(name_file)[-1]
    print(extension)
    if extension == '.txt':
        print('read txt')
        content = file_service.read_file(path_to_file=path)
    elif extension == '.json':
        content = file_service.read_json_file(path_to_file=path)
    elif extension == '.xlsx':
        content = file_service.read_excel_file(path_to_file=path)
    elif extension == '.csv':
        content = file_service.read_csv_file(path_to_file=path)
    else:
        content = ''
    print(content)
    return render_template('output_file.html', content=content, extension=extension)


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Configuration.ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print(request.url)
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file. Please choose the file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    return render_template('upload_file.html')


@app.route('/parse-rules', methods=['GET', 'POST'])
def pars_rules():
    content = file_service.parse_rules('InputOutputValidation_v2.xlsx')

    return render_template('parse_rules.html', content=content)


if __name__ == '__main__':
    app.run(debug=True)