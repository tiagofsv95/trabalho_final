from flask import request
from flask import jsonify
from flask import make_response
import sqlite3
from sqlite3 import Error
import os
import uuid
from passlib.hash import sha256_crypt
import jwt_lib_api

dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'
secret_key = '223d81adc68996234dd0734219aac254'

#######################################################
# 1. Criar usuario
def create_user():

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
            resp = make_response(jsonify({'error': 'Erro na requisição. Senhas sao diferentes.'}), 400)
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
                resp = make_response(jsonify({'error': 'O email ' + email + ' já está cadastrado.'}), 400)
                return resp

            sql = ''' INSERT INTO Usuario (id, nome, email, rua, numero, bairro, cep, cidadeId, estadoId, sexoId, telefone, password)
                                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
            cur = conn.cursor()
            cur.execute(sql, registro)

            json_obj = dict(zip(names, registro))
            del json_obj['password']
            json_data = [json_obj]

            conn.commit()
            resp = make_response(jsonify(json_data), 200)
            return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
            return resp
        finally:
            conn.close()
    else:
        resp = make_response(jsonify({'error': 'Erro na requisição.'}), 400)
        return resp

#######################################################
# 2. Buscar usuarios todos os usuarios
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
                del json_obj['password']
                json_data.append(json_obj)

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

#######################################################
# 3. Buscar usuario pelo id
def get_user_by_id(iduser=None):
    if iduser == None:
        resp = make_response(jsonify({'error': 'Parametro id do usuario invalido.'}), 400)
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
                json_data = json_obj

                sql = '''SELECT * FROM Sexo WHERE id = ''' + '"' + json_data['sexoId'] + '"'
                cur = conn.cursor()
                cur.execute(sql)
                Sexo = cur.fetchone()
                json_data['Sexo'] = Sexo

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

#######################################################
# 4. Atualizar usuarios pelo id
def update_user(iduser):
    if iduser == None:
        resp = make_response(jsonify({'error': 'Parametro id usuario invalido.'}), 400)
        return resp
    else:
        try:
            nome = request.json['nome']
            rua = request.json['rua']
            numero = request.json['numero']
            bairro = request.json['bairro']
            cep = request.json['cep']
            cidadeId = request.json['cidadeId']
            estadoId = request.json['estadoId']
            telefone = request.json['telefone']

            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Usuario WHERE id = ''' + '"' + iduser + '"'
            cur = conn.cursor()
            cur.execute(sql)
            usuario = cur.fetchone()

            if usuario:
                names = [description[0] for description in cur.description]
                json_obj = dict(zip(names, usuario))
                if request.json and usuario:
                    if 'nome' not in request.json:
                        nome = json_obj['nome']

                    if 'rua' not in request.json:
                        rua = json_obj['rua']

                    if 'numero' not in request.json:
                        numero = json_obj['numero']

                    if 'bairro' not in request.json:
                        bairro = json_obj['bairro']

                    if 'cep' not in request.json:
                        cep = json_obj['cep']

                    if 'cidadeId' not in request.json:
                        cidadeId = json_obj['cidadeId']

                    if 'estadoId' not in request.json:
                        estadoId = json_obj['estadoId']

                    if 'telefone' not in request.json:
                        telefone = json_obj['telefone']

                    registro = (nome, rua, numero, bairro, cep, cidadeId, estadoId, telefone)

                    sql = ''' UPDATE Usuario
                                            SET nome = ?, rua = ?, numero = ?, bairro = ?, cep = ?, cidadeId = ?, estadoId = ?, telefone = ?
                                            WHERE id = ''' + '"' + iduser + '"'
                    cur = conn.cursor()
                    cur.execute(sql, registro)
                    conn.commit()

                    sql = '''SELECT * FROM Usuario WHERE id = ''' + '"' + iduser + '"'
                    cur = conn.cursor()
                    cur.execute(sql)
                    updated_user = cur.fetchone()

                    json_obj = dict(zip(names, updated_user))
                    del json_obj['password']
                    json_data = [json_obj]

                    resp = make_response(jsonify(json_data), 200)
                    return resp

            else:
                resp = make_response(jsonify({'error': 'Usuario nao encontrado.'}), 400)
                return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
            return resp
        finally:
            conn.close()


#######################################################
# 5. Deletar usuarios pelo id
def delete_user(iduser=None):
    if iduser == None:
        resp = make_response(jsonify({'error': 'Parametro idproduto invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''DELETE FROM Usuario WHERE id = ''' + '"' + iduser + '"'
            cur = conn.cursor()
            cur.execute(sql)

            conn.commit()

            resp = make_response(jsonify({'error': 'Registro deletado com sucesso.'}), 200)
            return resp
        except Error as e:
            print(e)
            resp = make_response(jsonify({'error': e}), 500)
            return resp
        finally:
            conn.close()

#######################################################
# 6. Autenticar usuario
def auth_user():
    email = request.json['email']
    password = request.json['senha']

    if email and password:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Usuario WHERE email = ''' + '"' + email + '"'
            cur = conn.cursor()
            cur.execute(sql)
            usuario = cur.fetchone()

            if usuario:
                names = [description[0] for description in cur.description]
                usuario_obj = dict(zip(names, usuario))
                if (sha256_crypt.verify(password, usuario_obj['password'])):
                    token = jwt_lib_api.create_token(email, 60, secret_key)
                    del usuario_obj['password']
                    json_respose_obj = {
                        'auth': True,
                        'token': token,
                        'usuario': usuario_obj,
                        'message': 'Usuario autenticado com sucesso!'
                    }

                    resp = make_response(jsonify(json_respose_obj), 200)
                    return resp

                else:
                    resp = make_response(jsonify({'error': 'Email ou senha incorretos!'}), 400)
                    return resp

            else:
                resp = make_response(jsonify({'error': 'Email ou senha incorretos!'}), 400)
                return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
            return resp

        finally:
            conn.close()
    else:
        resp = make_response(jsonify({'error': 'Campo email ou senha vazios!'}), 400)
        return resp


#######################################################
# 7. Deslogar usuario
def logout_user():
    logout_obj = {
        'auth': False, 'token': None
    }
    resp = make_response(jsonify(logout_obj), 200)
    return resp
