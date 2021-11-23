from flask import Flask
from flask import request
from flask import jsonify
from datetime import datetime
from flask import make_response
import sqlite3
from sqlite3 import Error
import os
import uuid
import breed_routes
import breed_size_routes
import user_routes

#######################################################
# Instancia da Aplicacao Flask
app = Flask(__name__)
dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'

#######################################################
# 0. Testar aplicação
@app.route('/teste', methods=['GET'])
def test_get():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp


#######################################################
# ROUTAS USUARIOS
#######################################################

#######################################################
# 1. Criar usuario
@app.route('/usuario', methods=['POST'])
def create_user():
    return user_routes.create_user()

#######################################################
# 2. Buscar usuarios por nome
@app.route('/usuarios/nome', methods=['GET'])
def get_all_users_by_name():
    return user_routes.get_all_users_by_name()

#######################################################
# 3. Buscar usuarios todos os usuarios
@app.route('/usuarios', methods=['GET'])
def get_all_users():
    return user_routes.get_all_users()

#######################################################
# 4. Buscar usuario pelo id
@app.route('/usuario/<iduser>', methods=['GET'])
def get_user_by_id(iduser=None):
    return user_routes.get_user_by_id(iduser)

#######################################################
# 5. Atualizar usuarios pelo id
@app.route('/usuario/<iduser>', methods=['PUT'])
def update_user():
    return user_routes.update_user()

#######################################################
# 6. Deletar usuarios pelo id
@app.route('/usuario/<iduser>', methods=['DELETE'])
def delete_user():
    return user_routes.delete_user()

#######################################################
# 7. Autenticar usuario
@app.route('/autenticarUsuario', methods=['POST'])
def auth_user():
    return user_routes.auth_user()

#######################################################
# 8. Deslogar usuario
@app.route('/deslogarUsuario', methods=['POST'])
def logout_user():
    return user_routes.logout_user()


#######################################################
# ROTAS RAÇA
#######################################################

#######################################################
# 1. Buscar todas as raças
@app.route('/racas', methods=['GET'])
def get_all_breed():
    return breed_routes.get_all_breed()

#######################################################
# 2. Buscar raça pelo id
@app.route('/raca/<idbreed>', methods=['GET'])
def get_breed_by_id(idbreed=None):
    return breed_routes.get_breed_by_id(idbreed)

#######################################################
# 3. Buscar todas as raças por porte
@app.route('/racas/<sizeId>', methods=['GET'])
def get_breed_by_size(sizeId=None):
    return breed_routes.get_breed_by_size(sizeId)


#######################################################
# ROTAS PORTE
#######################################################

#######################################################
# 1. Buscar usuario pelo id
@app.route('/portes', methods=['GET'])
def get_all_size():
    return breed_size_routes.get_all_size()


#######################################################
# ROTAS CACHORRO
#######################################################

#######################################################
# 1. Cadastrar cachorro
@app.route('/cachorro', methods=['POST'])
def create_dog():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 2. Atualizar cachorro
@app.route('/cachorro', methods=['PUT'])
def update_dog():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

#######################################################
# 1. Buscar cachorro pelo id
@app.route('/cachorro/<iddog>', methods=['DELETE'])
def delete_dog():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

# 1. Buscar usuario pelo id
@app.route('/cachorro/<iddog>', methods=['GET'])
def get_dog_by_id():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

# 1. Buscar usuario pelo id
@app.route('/usuarioCachorros/<iduser>', methods=['GET'])
def get_dogs_by_user():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

# 1. Buscar usuario pelo id
@app.route('/cachorros', methods=['GET'])
def get_all_dogs():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp

# 1. Buscar usuario pelo id
@app.route('/informacoes', methods=['GET'])
def get_info():
    resp = make_response(jsonify({'mensagem': 'APPLICATION UP.'}), 200)
    return resp


#######################################################
# 1. Cadastrar produtos
@app.route('/produtos/cadastrar', methods=['POST'])
def cadastrar():
    descricao = None
    precocompra = None
    precovenda = None

    idproduto = str(uuid.uuid4())
    descricao = request.json['descricao']
    precocompra = request.json['precocompra']
    precovenda = request.json['precovenda']
    datacriacao = datetime.now()

    if idproduto and descricao and precocompra and precovenda and datacriacao:
        registro = (idproduto, descricao, precocompra, precovenda, datacriacao)
        names = ['idproduto', 'descricao', 'precocompra', 'precovenda', 'datacriacao']
        try:
            conn = sqlite3.connect(dirname + '/DB/dbprodutos.db')
            sql = ''' INSERT INTO produtos(idproduto, descricao, precocompra, precovenda, datacriacao)
                        VALUES(?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, registro)

            json_data = []
            json_data.append(dict(zip(names, registro)))

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
# 2. Listar produtos
@app.route('/produtos/listar', methods=['GET'])
def listar():
    try:
        conn = sqlite3.connect(dirname + '/DB/dbprodutos.db')
        sql = '''SELECT * FROM produtos'''
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
# 3. Alterar produtos
@app.route('/produtos/atualizar-por-id/<idproduto>', methods=['PUT'])
def alterar(idproduto=None):
    if idproduto == None:
        resp = make_response(jsonify({'mensagem': 'Parametro idproduto invalido.'}), 400)
        return resp
    else:
        try:
            descricao = None
            precocompra = None
            precovenda = None

            conn = sqlite3.connect(dirname + '/DB/dbprodutos.db')
            sql = '''SELECT * FROM produtos WHERE idproduto = ''' + '"' + idproduto + '"'
            cur = conn.cursor()
            cur.execute(sql)
            registro = cur.fetchone()

            if registro:
                if request.json and registro:
                    if 'descricao' in request.json:
                        descricao = request.json['descricao']
                    else:
                        descricao = registro[1]

                    if 'precocompra' in request.json:
                        precocompra = request.json['precocompra']
                    else:
                        precocompra = registro[2]

                    if 'precovenda' in request.json:
                        precovenda = request.json['precovenda']
                    else:
                        precovenda = registro[3]

                    datacriacao = registro[4]

                registro = (idproduto, descricao, precocompra, precovenda, datacriacao)

                sql = ''' UPDATE produtos
                        SET idproduto = ?, descricao = ?, precocompra = ?, precovenda = ?, datacriacao = ?
                        WHERE idproduto = ''' + '"' + idproduto + '"'
                cur = conn.cursor()
                cur.execute(sql, registro)

                names = ['idproduto', 'descricao', 'precocompra', 'precovenda', 'datacriacao']

                json_data = []
                json_data.append(dict(zip(names, registro)))

                conn.commit()
                resp = make_response(jsonify(json_data), 200)
                return resp
            else:
                resp = make_response(jsonify({'mensagem': 'Produto nao encontrado.'}), 400)
                return resp

        except Error as e:
            resp = make_response(jsonify({'mensagem': e}), 500)
            return resp
        finally:
            conn.close()


#######################################################
# 4. Deletar produtos
@app.route('/produtos/deletar/<idproduto>', methods=['DELETE'])
def deletar(idproduto=None):
    if idproduto == None:
        resp = make_response(jsonify({'mensagem': 'Parametro idproduto invalido.'}), 400)
        return resp
    else:
        try:
            conn = sqlite3.connect(dirname + '/DB/dbprodutos.db')
            sql = '''DELETE FROM produtos WHERE idproduto = ''' + '"' + idproduto + '"'
            cur = conn.cursor()
            cur.execute(sql)

            conn.commit()

            resp = make_response(jsonify({'mensagem': 'Registro deletado com sucesso.'}), 200)
            return resp
        except Error as e:
            print(e)
            resp = make_response(jsonify({'mensagem': e}), 500)
            return resp
        finally:
            conn.close()

#######################################################
# Rota de Erro
@app.errorhandler(404)
def rota_nao_encontrada(e):
    resp = make_response(jsonify({'mensagem': 'Rota não foi encontrada.'}), 404)
    return resp

#######################################################
# Execucao da Aplicacao
if __name__ == '__main__':
    app.run()