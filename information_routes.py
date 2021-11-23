from flask import request
from flask import jsonify
from datetime import datetime
from flask import make_response
import sqlite3
from sqlite3 import Error
import os
import uuid

# 1. Buscar informaçoes
def get_info():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp
