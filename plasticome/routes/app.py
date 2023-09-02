from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec

from plasticome.controllers.fungi_controller import (
    search_fungi_by_name
)
from plasticome.controllers.pipeline_controller import execute_main_pipeline


server = Flask(__name__)
spec = FlaskPydanticSpec(
    'flask', title='PLASTICOME DEMO',version='v1.0', path='docs'
)
spec.register(server)


@server.get('/')
def get_plasticome():
    return 'Plasticome server is running!'


@server.get('/fungi/<fungi_name>')
def get_fungi_id_by_name(fungi_name):
    return search_fungi_by_name(fungi_name)


@server.post('/analyze')
def execute_pipeline():
    return execute_main_pipeline(request.json)


server.run()
