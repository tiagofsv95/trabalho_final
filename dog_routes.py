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
            resp = make_response(jsonify({'error': e}), 500)
            return resp
        finally:
            conn.close()
    else:
        resp = make_response(jsonify({'error': 'Erro na requisição.'}), 400)
        return resp


#######################################################
# 2. Atualizar cachorro
def update_dog():
    iddog = request.json['id']
    usuarioId = request.json['usuarioId']

    if iddog == None or usuarioId == None:
        resp = make_response(jsonify({'error': 'Parametro id usuario invalido.'}), 400)
        return resp
    else:
        try:
            nome = request.json['nome']
            racaId = request.json['racaId']
            sexoId = request.json['sexoId']
            informacoes = request.json['informacoes']
            rua = request.json['rua']
            numero = request.json['numero']
            bairro = request.json['bairro']
            cep = request.json['cep']
            cidadeId = request.json['cidadeId']
            estadoId = request.json['estadoId']
            adotado = request.json['adotado']
            mostrarEndereco = request.json['mostrarEndereco']

            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
            cur = conn.cursor()
            cur.execute(sql)
            cachorro = cur.fetchone()

            if cachorro:
                names = [description[0] for description in cur.description]
                json_obj = dict(zip(names, cachorro))
                if request.json and cachorro:
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

                    if 'racaId' not in request.json:
                        racaId = json_obj['racaId']

                    if 'sexoId' not in request.json:
                        sexoId = json_obj['sexoId']

                    if 'informacoes' not in request.json:
                        informacoes = json_obj['informacoes']

                    if 'adotado' not in request.json:
                        adotado = json_obj['adotado']

                    if 'mostrarEndereco' not in request.json:
                        mostrarEndereco = json_obj['mostrarEndereco']

                    registro = (nome, rua, numero, bairro, cep, cidadeId, estadoId, racaId, sexoId, informacoes, adotado, mostrarEndereco, usuarioId)

                    sql = ''' UPDATE Cachorro
                                            SET nome = ?, rua = ?, numero = ?, bairro = ?, cep = ?, cidadeId = ?, racaId = ?, 
                                            sexoId = ?, informacoes = ?, adotado = ?, mostrarEndereco = ?, usuarioId = ?
                                            WHERE id = ''' + '"' + iddog + '"'
                    cur = conn.cursor()
                    cur.execute(sql, registro)
                    conn.commit()

                    sql = '''SELECT * FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
                    cur = conn.cursor()
                    cur.execute(sql)
                    updated_dog = cur.fetchone()

                    json_obj = dict(zip(names, updated_dog))
                    del json_obj['password']
                    json_data = [json_obj]

                    resp = make_response(jsonify(json_data), 200)
                    return resp

            else:
                resp = make_response(jsonify({'error': 'Cachorro nao encontrado.'}), 400)
                return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
            return resp
        finally:
            conn.close()

#######################################################
# 3. Deletar cachorro pelo id
def delete_dog(iddog):
    if iddog == None:
        resp = make_response(jsonify({'error': 'Parametro id cachorro invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(database_dirname)
            sql = '''DELETE FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
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
# 4. Buscar cachorro pelo id
def get_dog_by_id(iddog):
    if iddog == None:
        resp = make_response(jsonify({'error': 'Parametro id do cachorro invalido.'}), 400)
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
                resp = make_response(jsonify({'error': 'Registro não encontrado.'}), 204)
                return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
            return resp

        finally:
            conn.close()


#######################################################
# 5. Buscar cachorro pelo usuario
def get_dogs_by_user(iduser):
    if iduser == None:
        resp = make_response(jsonify({'error': 'Parametro id do usuario invalido.'}), 400)
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
                resp = make_response(jsonify({'error': 'Registro não encontrado.'}), 204)
                return resp

        except Error as e:
            resp = make_response(jsonify({'error': e}), 500)
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
            resp = make_response(jsonify({'error': 'Registro não encontrado.'}), 204)
            return resp

    except Error as e:
        resp = make_response(jsonify({'error': e}), 500)
        return resp

    finally:
        conn.close()
