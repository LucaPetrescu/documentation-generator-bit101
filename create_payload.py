import json


s= """
from flask import Blueprint, request, abort
from sqlalchemy import and_
from docgen import Loader
from schemas import ResponseSchema
from models.responses import ResponseModel
from docgen import Loader, write_response
from db import db


blp = Blueprint('back-end', __name__)

@blp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@blp.route('/askdoc/', methods=['POST'])
def askdoc():
    api_key = request.headers.get('Openai-key')
    payload = request.get_json()
    errors = ResponseSchema().validate(payload)
    if errors:
        abort(400, str(errors))
    
    conversation = ResponseModel.query.filter(and_(ResponseModel.message == payload['message'],
                                                   ResponseModel.response_type == 'doc')).first()
    if conversation is None:
        loader = Loader(api_key, payload['message'])

        documentation=''
        documentation = loader.get_response_doc()

        write_response(dir='results', content=payload['message'] + 'doc', response=documentation)
        
        conversation = ResponseModel(message=payload['message'],
                                 response=documentation,
                                 response_type='doc')
        db.session.add(conversation)
        db.session.commit()

    return ResponseSchema().dump(conversation), 200

@blp.route('/askupdate', methods=['POST'])
def askupdate():
    api_key = request.headers.get('Openai-key')
    payload = request.get_json()
    errors = ResponseSchema().validate(payload)
    if errors:
        abort(400, str(errors))
    
    conversation = ResponseModel.query.filter(and_(ResponseModel.message == payload['message'],
                                                   ResponseModel.response_type == 'update')).first()
    if conversation is None:
        loader = Loader(api_key, payload['message'])

        documentation=''
        documentation = loader.get_response_update()
        
        write_response(dir='results', content=payload['message'] + 'update', response=documentation)

        conversation = ResponseModel(message=payload['message'],
                                 response=documentation,
                                 response_type='update')
        db.session.add(conversation)
        db.session.commit()

    return ResponseSchema().dump(conversation), 200
"""

payload = {'message': s}
payload_json = json.dumps(payload)
print(payload_json)
