from flask import jsonify
from datetime import datetime
from flask import make_response
import sqlite3
from sqlite3 import Error
import os

dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'

#######################################################
# 1. Buscar informaçoes
def get_info():
    try:
        conn = sqlite3.connect(database_dirname)

        sql = '''SELECT id, descricao FROM Porte'''
        cur = conn.cursor()
        cur.execute(sql)
        portes = cur.fetchall()
        portes_json_obj = []
        for reg in portes:
            portes_json_obj.append(dict(zip(['id','descricao'], reg)))

        sql = '''SELECT * FROM Raca'''
        cur = conn.cursor()
        cur.execute(sql)
        racas = cur.fetchall()
        names_racas = [description[0] for description in cur.description]
        racas_json_obj = []
        for reg in racas:
            racas_json_obj.append(dict(zip(names_racas, reg)))

        sql = '''SELECT id, descricao FROM Sexo WHERE tipo = "animal"'''
        cur = conn.cursor()
        cur.execute(sql)
        sexos_animais = cur.fetchall()
        sexos_animais_json_obj = []
        for reg in sexos_animais:
            sexos_animais_json_obj.append(dict(zip(['id', 'descricao'], reg)))

        sql = '''SELECT id, descricao FROM Sexo WHERE tipo = "serHumano"'''
        cur = conn.cursor()
        cur.execute(sql)
        sexos_seres_humanos = cur.fetchall()
        sexos_seres_humanos_json_obj = []
        for reg in sexos_seres_humanos:
            sexos_seres_humanos_json_obj.append(dict(zip(['id', 'descricao'], reg)))

        sql = '''SELECT id, nome FROM Estado'''
        cur = conn.cursor()
        cur.execute(sql)
        estados = cur.fetchall()
        estados_json_obj = []
        for reg in estados:
            estados_json_obj.append(dict(zip(['id', 'nome'], reg)))

        sql = '''SELECT id, nome, estadoId FROM Municipio'''
        cur = conn.cursor()
        cur.execute(sql)
        municipios = cur.fetchall()
        municipios_json_obj = []
        for reg in municipios:
            municipios_json_obj.append(dict(zip(['id', 'nome'], reg)))

        registro = (portes_json_obj, racas_json_obj, sexos_animais_json_obj, sexos_seres_humanos_json_obj, estados_json_obj, municipios_json_obj)
        json_data = dict(zip(['portes', 'racas', 'sexosAnimais', 'sexosSeresHumanos', 'estados', 'municipios'], registro))

        resp = make_response(jsonify(json_data), 200)
        return resp

    except Error as e:
        resp = make_response(jsonify({'error': e}), 500)
        return resp

    finally:
        conn.close()
