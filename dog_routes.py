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
    cachorro = request.json
    for attr, value in cachorro.items():
        if (not value and attr != 'foto') and (not value and attr != 'informacoes') and (not value and attr != 'adotado'):
            resp = make_response(jsonify({'mensagem': 'Erro na requisição. Campo ' + attr + ' sem registro.'}), 400)
            return resp

    nome = request.json['nome']
    informacoes = request.json['informacoes']
    rua = request.json['rua']
    numero = request.json['numero']
    bairro = request.json['bairro']
    cep = request.json['cep']
    cidadeId = request.json['cidadeId']
    estadoId = request.json['estadoId']
    sexoId = request.json['sexoId']
    racaId = request.json['racaId']
    usuarioId = request.json['usuarioId']
    mostrarEndereco = request.json['mostrarEndereco']
    adotado = request.json['adotado']
    foto = request.json['foto']

    if nome and rua and numero and bairro and cep and cidadeId and estadoId and sexoId and racaId and usuarioId and mostrarEndereco:
        id_cachorro = str(uuid.uuid4())

        registro = (id_cachorro, nome, informacoes, rua, numero, bairro, cep, cidadeId, estadoId, sexoId, racaId, usuarioId, mostrarEndereco, adotado, foto)
        names = ['id', 'nome', 'informacoes', 'rua', 'numero', 'bairro', 'cep', 'cidadeId', 'estadoId', 'sexoId', 'racaId', 'usuarioId', 'mostrarEndereco', 'adotado', 'foto']
        try:
            conn = sqlite3.connect(database_dirname)
            sql = ''' INSERT INTO Cachorro (id, nome, informacoes, rua, numero, bairro, cep, cidadeId, estadoId, sexoId, racaId, usuarioId, mostrarEndereco, adotado, foto)
                                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
            cur = conn.cursor()
            cur.execute(sql, registro)
            json_data = [dict(zip(names, registro))]

            conn.commit()
            resp = make_response(jsonify(json_data), 200)
            return resp

        except Error as e:
            resp = make_response(jsonify({'mensagem': e}), 500)
            return resp
        finally:
            conn.close()
    else:
        resp = make_response(jsonify({'mensagem': 'Erro na requisição.'}), 400)
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
def get_dog_by_id(iddog):
    if iddog == None:
        resp = make_response(jsonify({'mensagem': 'Parametro id do cachorro invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
            cur = conn.cursor()
            cur.execute(sql)
            registro = cur.fetchone()

            if registro:
                names = [description[0] for description in cur.description]
                json_data = [dict(zip(names, registro))]
                resp = make_response(jsonify(json_data), 200)
                return resp

            else:
                resp = make_response(jsonify({'mensagem': 'Registro não encontrado.'}), 204)
                return resp

        except Error as e:
            resp = make_response(jsonify({'mensagem': e}), 500)
            return resp

        finally:
            conn.close()


#######################################################
# 5. Buscar cachorro pelo usuario
def get_dogs_by_user(iduser):
    if iduser == None:
        resp = make_response(jsonify({'mensagem': 'Parametro id do usuario invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Cachorro WHERE usuarioId = ''' + '"' + iduser + '"'
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
                resp = make_response(jsonify({'mensagem': 'Registro não encontrado.'}), 204)
                return resp

        except Error as e:
            resp = make_response(jsonify({'mensagem': e}), 500)
            return resp

        finally:
            conn.close()

#######################################################
# 6. Buscar todos os cachorros
def get_all_dogs():
    try:
        conn = sqlite3.connect(database_dirname)
        sql = '''SELECT * FROM Cachorro'''
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
            resp = make_response(jsonify({'mensagem': 'Registro não encontrado.'}), 204)
            return resp

    except Error as e:
        resp = make_response(jsonify({'mensagem': e}), 500)
        return resp

    finally:
        conn.close()
