import os
from flask import Flask, render_template, redirect, url_for, request, flash, \
    send_from_directory
import file_service
from config import Configuration
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object(Configuration)


def define_path_to_file(file_name):
    return os.path.join(os.getcwd(), 'tests_file', file_name)


@app.route('/')
def index():
    files = [file for file in os.listdir(os.path.join(os.getcwd(), 'tests_file'))]
    return render_template('index.html', files=files)


@app.route('/delete/<file_name>', methods=['POST'])
def delete_file(file_name):
    path_to_file = define_path_to_file(file_name)
    file_service.delete_file(path_to_file)
    return redirect(url_for('index'))


@app.route('/read_file/<file_name>')
def read_file(file_name):
    path = define_path_to_file(file_name)
    extension = os.path.splitext(file_name)[-1]
    if extension == '.txt':
        content = file_service.read_file(path_to_file=path)
    elif extension == '.json':
        content = file_service.read_json_file(path_to_file=path)
    elif extension == '.xlsx':
        content = file_service.read_excel_file(path_to_file=path)
    elif extension == '.csv':
        content = file_service.read_csv_file(path_to_file=path)
    else:
        content = ''
    return render_template('output_file.html', content=content, extension=extension)


@app.route('/update/<file_name>', methods=['GET', 'POST'])
def update_file(file_name):
    path = define_path_to_file(file_name)
    if request.method == 'POST':
        content = request.form.get('content', '')

        with open(path, 'w') as file:
            file.write(content)

        flash(f'File {file_name} was successfully updated', category='success')
        return redirect(url_for('index'))

    content = file_service.read_file(path)
    return render_template('update_file.html', content=content)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Configuration.ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file. Please choose the file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'File {file.filename} was successfully uploaded', category='success')
            return redirect(url_for('index'))

    return render_template('upload_file.html')


@app.route('/parse-rules', methods=['GET', 'POST'])
def pars_rules():
    content = [['Rule ID', 'Rule description', 'Result formula', 'Result amount', 'Status', 'LHS', 'RHS']]
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file. Please choose the file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = define_path_to_file(filename)
            content = file_service.parse_rules(path)

    return render_template('parse_rules.html', content=content)


@app.route('/get-meta-data/<file_name>')
def get_meta_data(file_name):
    path = define_path_to_file(file_name)
    data = file_service.get_metadata_file(path)
    return data


if __name__ == '__main__':
    app.run(debug=True)