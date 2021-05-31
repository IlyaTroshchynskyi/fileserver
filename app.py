import os
import logging
from flask import Flask, render_template, redirect, url_for, request, flash, \
    send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security, login_required, current_user
from config import init_logger, Configuration, TEST_FILES_DIR
import file_service

init_logger('app')
logger = logging.getLogger("app.main")

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
mg = Migrate(app, db)
from models import User, Role
users = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, users)


def define_path_to_file(file_name):
    """Define path to file on the server
    Args:
        file_name (srt): File name
    Returns:
        path (str): Return path to file
    """
    return os.path.join(os.getcwd(), TEST_FILES_DIR, file_name)


@app.route('/')
def index():
    """Show files on the server in browser
    """
    files_per_page = 5
    page = request.args.get('page', '1')
    if page.isdigit():
        page = int(page)
    else:
        page = 1
    logger.info(f'Current page:{page}')
    working_dir = os.path.join(os.getcwd(), TEST_FILES_DIR)
    files = [file for file in os.listdir(working_dir) if os.path.isfile(f'{working_dir}/{file}')]
    last_page = int(len(files)/5)
    return render_template('index.html',
                           files=files[(page-1) * files_per_page:(page-1) * files_per_page+files_per_page],
                           count_files=range(page, page+2 if page <= last_page-2 else last_page),
                           cur_page=page, last_page=last_page)


@app.route('/delete/<file_name>', methods=['POST', 'GET'])
@login_required
def delete_file(file_name):

    path_to_file = define_path_to_file(file_name)
    file_service.delete_file(path_to_file)
    return redirect(url_for('index'))


@app.route('/read_file/<file_name>')
@login_required
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
    logger.info(f'Content: "{content}" for file: "{file_name}"')
    return render_template('output_file.html', content=content, extension=extension)


@app.route('/update/<file_name>', methods=['GET', 'POST'])
@login_required
def update_file(file_name):
    path = define_path_to_file(file_name)
    if request.method == 'POST':
        content = request.form.get('content', '')

        file_service.update_file_txt(path, content)
        logger.info(f'File: "{file_name}" was successfully updated with contetn "{content}"')
        flash(f'File {file_name} was successfully updated', category='success')
        return redirect(url_for('index'))

    content = file_service.read_file(path)
    return render_template('update_file.html', content=content)


def allowed_file(filename):
    """Split file name by the '.' and check the allowed extension
    Args:
        filename (srt): File name
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Configuration.ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Upload file on the server to upload directory
    Args:
        filename (srt): File name
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload_file', methods=['GET', 'POST'])
@login_required
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
            flash(f'File {file.filename} was successfully uploaded', 'success')
            logger.info(f'File {file.filename} was successfully uploaded to {Configuration.UPLOAD_FOLDER}')
            return redirect(url_for('index'))

    return render_template('upload_file.html')


@app.route('/parse-rules', methods=['GET', 'POST'])
@login_required
def parse_rules():
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
@login_required
def get_meta_data(file_name):
    path = define_path_to_file(file_name)
    data = file_service.get_metadata_file(path)
    return data


@app.route('/create-file', methods=['GET', 'POST'])
@login_required
def create_file():
    length_name = extension = content = ''
    letter = digit = True
    if request.method == 'POST':
        length_name = int(request.form.get('length', ''))
        extension = request.form.get('extension', '')
        content = request.form.get('content', '')
        letter = True if request.form.get('letter', '') else False
        digit = True if request.form.get('digit', '') else False

        file_name = file_service.create_file(length_name=length_name,
                                 extension=extension,
                                 content=content,
                                 letter=letter,
                                 digit=digit)
        flash(f'File: "{file_name}" was created successfully', 'success')
        logger.info(f'File: "{file_name}" was created successfully')
        return redirect(url_for('index'))
    return render_template('create_file.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        password1 = request.form.get('password2', '')
        if password1 == password:
            users.create_user(email=email, password=password)
            db.session.commit()
            flash(f'Your account has been created! You are able to log in', 'success')
            logger.info(f'Account for user with email: "{email}" was created')
            return redirect(url_for('security.login'))
    return render_template('register_user.html')
