from flask import request
from flask import jsonify
from datetime import datetime
from flask import make_response
import sqlite3
from sqlite3 import Error
import os
import uuid

dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'

#######################################################
# 1. Cadastrar cachorro
def create_dog():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 2. Atualizar cachorro
def update_dog():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 3. Deletar cachorro pelo id
def delete_dog():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 4. Buscar cachorro pelo id
def get_dog_by_id():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 5. Buscar cachorro pelo usuario
def get_dogs_by_user():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 6. Buscar todos os cachorros
def get_all_dogs():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp
