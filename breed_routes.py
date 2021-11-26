from flask import jsonify
from flask import make_response
import sqlite3
from sqlite3 import Error
import os

dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'

def get_all_breed():
    try:
        conn = sqlite3.connect(database_dirname)
        sql = '''SELECT * FROM Raca'''
        cur = conn.cursor()
        cur.execute(sql)
        registros = cur.fetchall()

        if registros:
            names = [description[0] for description in cur.description]

            json_data = []
            for reg in registros:
                json_data.append(dict(zip(names, reg)))

            resp = make_response(jsonify(json_data), 200)
            return resp

        else:
            resp = make_response(jsonify({'error': 'Registro não encontrado.'}), 204)
            return resp

    except Error as e:
        resp = make_response(jsonify({'error': e}), 500)
        return resp

    finally:
        conn.close()

# 1. Buscar usuario pelo id
def get_breed_by_id(idbreed=None):
    if idbreed == None:
        resp = make_response(jsonify({'error': 'Parametro id raça invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Raca WHERE id = ''' + '"' + idbreed + '"'
            cur = conn.cursor()
            cur.execute(sql)
            registro = cur.fetchone()

            if registro:
                names = [description[0] for description in cur.description]
                json_data = [dict(zip(names, registro))]
                resp = make_response(jsonify(json_data), 200)
                return resp

            else:
                resp = make_response(jsonify({'error': 'Registro não encontrado.'}), 204)
                return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
            return resp

        finally:
            conn.close()

# 1. Buscar usuario pelo id
def get_breed_by_size(sizeId=None):
    if sizeId == None:
        resp = make_response(jsonify({'error': 'Parametro porteId da raça invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Raca WHERE porteId = ''' + '"' + sizeId + '"'
            cur = conn.cursor()
            cur.execute(sql)
            registros = cur.fetchall()

            if registros:
                names = [description[0] for description in cur.description]

                json_data = []
                for reg in registros:
                    json_data.append(dict(zip(names, reg)))

                resp = make_response(jsonify(json_data), 200)
                return resp

            else:
                resp = make_response(jsonify({'error': 'Registro não encontrado.'}), 204)
                return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
            return resp

        finally:
            conn.close()