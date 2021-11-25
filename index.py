from flask import Flask, request, jsonify, make_response, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
from sqlite3 import Error
import os
import breed_routes
import breed_size_routes
import user_routes
import dog_routes
import information_routes
import jwt_lib_api

#######################################################
# Instancia da Aplicacao Flask
app = Flask(__name__)
dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'
secret_key = '223d81adc68996234dd0734219aac254'

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
# 2. Buscar usuarios todos os usuarios
@app.route('/usuarios', methods=['GET'])
def get_all_users():
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return user_routes.get_all_users()

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 3. Buscar usuario pelo id
@app.route('/usuario/<iduser>', methods=['GET'])
def get_user_by_id(iduser=None):
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return user_routes.get_user_by_id(iduser)

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 4. Atualizar usuarios pelo id
@app.route('/usuario/<iduser>', methods=['PUT'])
def update_user(iduser=None):
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return user_routes.update_user(iduser)

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 5. Deletar usuarios pelo id
@app.route('/usuario/<iduser>', methods=['DELETE'])
def delete_user(iduser=None):
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return user_routes.delete_user(iduser)

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp


#######################################################
# 6. Autenticar usuario
@app.route('/autenticarUsuario', methods=['POST'])
def auth_user():
    return user_routes.auth_user()

#######################################################
# 7. Deslogar usuario
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
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return breed_routes.get_breed_by_id(idbreed)

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 3. Buscar todas as raças por porte
@app.route('/racas/<sizeId>', methods=['GET'])
def get_breed_by_size(sizeId=None):
    return breed_routes.get_breed_by_size(sizeId)


#######################################################
# ROTA PORTE
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
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return dog_routes.create_dog()

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 2. Atualizar cachorro
@app.route('/cachorro', methods=['PUT'])
def update_dog():
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return dog_routes.update_dog()

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 3. Deletar cachorro
@app.route('/cachorro/<iddog>', methods=['DELETE'])
def delete_dog(iddog=None):
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return dog_routes.delete_dog(iddog)

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 4. Buscar cachorro pelo id
@app.route('/cachorro/<iddog>', methods=['GET'])
def get_dog_by_id(iddog=None):
    token = request.headers['Authorization'].replace("Bearer ", "")
    is_verified = jwt_lib_api.verify_token(token, secret_key)
    if (is_verified):
        return dog_routes.get_dog_by_id(iddog)

    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
        return resp

#######################################################
# 5. Buscar cachorro por usuario
@app.route('/usuarioCachorros/<iduser>', methods=['GET'])
def get_dogs_by_user(iduser=None):
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
        is_verified = jwt_lib_api.verify_token(token, secret_key)
        if (is_verified):
            return dog_routes.get_dogs_by_user(iduser)
        else:
            resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
            return resp
    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Nao conseguimos identificar o seu token de acesso.'}), 401)
        return resp

#######################################################
# 6. Buscar todos os cachorros
@app.route('/cachorros', methods=['GET'])
def get_all_dogs():
    return dog_routes.get_all_dogs()


#######################################################
# ROTA INFORMAÇOES
#######################################################

# 1. Buscar informaçoes
@app.route('/informacoes', methods=['GET'])
def get_info():
    return information_routes.get_info()


#######################################################
# ROTA DE UPLOADS
#######################################################

# 1. Buscar informaçoes
@app.route('/fotoPerfil', methods=['POST'])
def upload_profile_photo(userid=None):
    iduser = request.args.get('id')
    if not os.path.isdir(dirname+'/uploads/perfil/'+iduser):
        os.mkdir(dirname+'/uploads/perfil/'+iduser)
    file = request.files['foto']
    if file.filename == '':
        print('No selected file')
    else:
        try:

            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Usuario WHERE id = ''' + '"' + iduser + '"'
            cur = conn.cursor()
            cur.execute(sql)
            usuario = cur.fetchone()

            if usuario:

                filename = secure_filename(file.filename)
                file.save(os.path.join(dirname+'/uploads/perfil/'+iduser, filename))
                foto = '/uploads/perfil/'+iduser+'/'+filename
                registro = (foto,)
                sql = ''' UPDATE Usuario SET foto = ?, numero = ? WHERE id = ''' + '"' + iduser + '"'
                cur = conn.cursor()
                print(registro)
                cur.execute(sql, registro)
                conn.commit()

                sql = '''SELECT * FROM Usuario WHERE id = ''' + '"' + iduser + '"'
                cur = conn.cursor()
                cur.execute(sql)
                updated_user = cur.fetchone()

                names = [description[0] for description in cur.description]

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


@app.route('/fotoPerfil/<iduser>', methods=['GET'])
def get_profile_photo(iduser=None):
    if iduser == None:
        resp = make_response(jsonify({'error': 'Parametro id usuario invalido.'}), 400)
        return resp
    else:
        conn = sqlite3.connect(database_dirname)
        sql = '''SELECT * FROM Usuario WHERE id = ''' + '"' + iduser + '"'
        cur = conn.cursor()
        cur.execute(sql)
        usuario = cur.fetchone()

        if usuario:
            names = [description[0] for description in cur.description]
            json_obj = dict(zip(names, usuario))
            print(json_obj['foto'])
            if json_obj['foto']:
                filename = os.path.basename(json_obj['foto'])
                pathname = json_obj['foto'].replace('/'+filename, '')
                print(filename)
                print(pathname)
                return send_from_directory(dirname+pathname, filename)

            else:
                resp = make_response(jsonify({'error': 'Foto do usuario nao encontrado.'}), 404)
                return resp
        else:
            resp = make_response(jsonify({'error': 'Usuario nao encontrado.'}), 400)
            return resp

#######################################################
# Rota de Erro
#######################################################
@app.errorhandler(404)
def rota_nao_encontrada(e):
    resp = make_response(jsonify({'mensagem': 'Rota não foi encontrada.'}), 404)
    return resp


#######################################################
# Execucao da Aplicacao
if __name__ == '__main__':
    app.run()
