import os
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import file_service
from app import define_path_to_file
from config import Configuration, TEST_FILES_DIR

app = Flask(__name__)
app.config.from_object(Configuration)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('content')


class ListFilesApi(Resource):

    def get(self, file_name):
        working_dir = os.path.join(os.getcwd(), TEST_FILES_DIR)
        files = [file for file in os.listdir(working_dir) if os.path.isfile(f'{working_dir}/{file}')]
        if os.path.isfile(define_path_to_file(file_name)):
            return {"all_files": files}
        elif file_name not in files:
            return {"message": "file wasn't found"}, 404
        else:
            return {"content": file_service.read_file(define_path_to_file(file_name))}

    def post(self):
        file_json = request.json
        length_name = file_json.get('length_name', 5)
        extension = file_json.get('extension', '.txt')
        content = file_json.get('content', '')
        letter = file_json.get('letter', True)
        digit = file_json.get('digit', True)
        return file_service.create_file(length_name, extension, content, letter, digit), 201

    def put(self, file_name):
        new_content = parser.parse_args()["content"]
        path = define_path_to_file(file_name)
        if os.path.isfile(path):
            file_service.update_file_txt(path, new_content)
            return {"content": file_service.read_file(path)}
        return {"message": "file wasn't found"}, 404

    def delete(self, file_name):
        if os.path.isfile(define_path_to_file(file_name)):
            file_service.delete_file(define_path_to_file(file_name))
            return '', 204
        return {"message": "file wasn't found"}, 404

class ListParseRules(Resource):

    def get(self, file_name):
        if os.path.isfile(define_path_to_file(file_name)):
            return {'result': file_service.parse_rules(define_path_to_file(file_name))}
        return {"message": "file wasn't found"}, 404


class MetaData(Resource):

    def get(self, file_name):
        if os.path.isfile(define_path_to_file(file_name)):
             return file_service.get_metadata_file(define_path_to_file(file_name))
        return {"message": "file wasn't found"}, 404


api.add_resource(ListFilesApi, '/files', '/files/<file_name>', strict_slashes=False)
api.add_resource(ListParseRules, '/parse-rules/<file_name>', strict_slashes=False)
api.add_resource(MetaData, '/get-meta-data/<file_name>', strict_slashes=False)


if __name__ == '__main__':
    app.run(debug=True)