from flask import request
from flask import jsonify
from flask import make_response
import sqlite3
from sqlite3 import Error
import os
import uuid
from passlib.hash import sha256_crypt

dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'

#######################################################
# 1. Criar usuario
def create_user():
    usuario = request.json
    for attr, value in usuario.items():
        if not value and attr != 'foto':
            resp = make_response(jsonify({'mensagem': 'Erro na requisição. Campo ' + attr + ' sem registro.'}), 400)
            return resp

    nome = request.json['nome']
    email = request.json['email']
    rua = request.json['rua']
    numero = request.json['numero']
    bairro = request.json['bairro']
    cep = request.json['cep']
    cidadeId = request.json['cidadeId']
    estadoId = request.json['estadoId']
    sexoId = request.json['sexoId']
    telefone = request.json['telefone']
    senha_um = request.json['senha_um']
    senha_dois = request.json['senha_dois']

    if nome and email and rua and numero and bairro and cep and cidadeId and estadoId and sexoId and telefone and senha_um and senha_dois:
        if senha_um != senha_dois:
            resp = make_response(jsonify({'mensagem': 'Erro na requisição. Senhas sao diferentes.'}), 400)
            return resp

        id_usuario = str(uuid.uuid4())
        password = sha256_crypt.hash(senha_um)

        registro = (id_usuario, nome, email, rua, numero, bairro, cep, cidadeId, estadoId, sexoId, telefone, password)
        names = ['id', 'nome', 'email', 'rua', 'numero', 'bairro', 'cep', 'cidadeId', 'estadoId', 'sexoId', 'telefone', 'password']
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Usuario WHERE email = ''' + '"' + email + '"'
            cur = conn.cursor()
            cur.execute(sql)
            registro_existe = cur.fetchone()

            if registro_existe:
                resp = make_response(jsonify({'mensagem': 'O email ' + email + ' já está cadastrado.'}), 400)
                return resp

            sql = ''' INSERT INTO Usuario (id, nome, email, rua, numero, bairro, cep, cidadeId, estadoId, sexoId, telefone, password)
                                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
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
# 2. Buscar usuarios por nome
def get_all_users_by_name():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 3. Buscar usuarios todos os usuarios
def get_all_users():
    try:
        conn = sqlite3.connect(database_dirname)
        sql = '''SELECT * FROM Usuario'''
        cur = conn.cursor()
        cur.execute(sql)
        registros = cur.fetchall()

        if registros:
            names = [description[0] for description in cur.description]

            json_data = []
            for reg in registros:
                json_obj = dict(zip(names, reg))
                #print(sha256_crypt.verify("12345678", json_obj['password']))
                del json_obj['password']
                json_data.append(json_obj)

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
# 4. Buscar usuario pelo id
def get_user_by_id(iduser=None):
    if iduser == None:
        resp = make_response(jsonify({'mensagem': 'Parametro id do usuario invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Usuario WHERE id = ''' + '"' + iduser + '"'
            cur = conn.cursor()
            cur.execute(sql)
            registro = cur.fetchone()

            if registro:
                names = [description[0] for description in cur.description]
                json_obj = dict(zip(names, registro))
                del json_obj['password']
                json_data = [json_obj]
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
# 5. Atualizar usuarios pelo id
def update_user():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 6. Deletar usuarios pelo id
def delete_user():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 7. Autenticar usuario
def auth_user():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 8. Deslogar usuario
def logout_user():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp
