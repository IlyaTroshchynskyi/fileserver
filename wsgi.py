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
parser.add_argument('meta')


class ListFilesApi(Resource):

    def get(self, file_name=None, meta=False):
        files = [file for file in os.listdir(os.path.join(os.getcwd(), TEST_FILES_DIR))]
        if not file_name:
            return {"all_files": files}
        elif file_name not in files:
            return '', 404
        elif parser.parse_args()["meta"]:
            return {"meta-data": file_service.get_metadata_file(define_path_to_file(file_name))}
        else:
            return {"content": file_service.read_file(define_path_to_file(file_name))}

    def post(self):
        file_json = request.json
        return file_service.create_file(*file_json.values())

    def put(self, file_name):
        new_content = parser.parse_args()["content"]
        path = define_path_to_file(file_name)
        file_service.update_file_txt(path, new_content)
        return {"content": file_service.read_file(path)}, 201

    def delete(self, file_name):
        file_service.delete_file(define_path_to_file(file_name))
        return '', 204


class ListParseRules(Resource):

    def get(self, file_name):
        return {'result': file_service.parse_rules(define_path_to_file(file_name))}


api.add_resource(ListFilesApi, '/files', '/files/<file_name>', strict_slashes=False)
api.add_resource(ListParseRules, '/parse-rules/<file_name>', strict_slashes=False)



if __name__ == '__main__':
    app.run(debug=True)