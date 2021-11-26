from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
import os
import breed_routes
import breed_size_routes
import user_routes
import dog_routes
import information_routes
import jwt_lib_api
import upload_routes

#######################################################
# Instancia da Aplicacao Flask
app = Flask(__name__)
CORS(app)
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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace("Bearer ", "")
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

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
    elif 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']

    print(token)

    is_verified = jwt_lib_api.verify_token(token, secret_key)

    print(is_verified)
    if (is_verified):
        return dog_routes.get_dogs_by_user(iduser)
    else:
        resp = make_response(jsonify({'auth': False, 'error': 'Seu login expirou !'}), 401)
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

#######################################################
# 1. Salvar foto de perfil
@app.route('/fotoPerfil', methods=['POST'])
def upload_profile_photo():
    return upload_routes.upload_profile_photo()


#######################################################
# 2. Obter foto de perfil
@app.route('/fotoPerfil/<iduser>', methods=['GET'])
def get_profile_photo(iduser=None):
    return upload_routes.get_profile_photo(iduser)


#######################################################
# 3. Deletar foto de perfil
@app.route('/fotoPerfil/<iduser>', methods=['DELETE'])
def delete_profile_photo(iduser=None):
    return upload_routes.delete_profile_photo(iduser)


#######################################################
# 4. Salvar foto de cachorro
@app.route('/fotoCachorro', methods=['POST'])
def upload_dog_photo():
    return upload_routes.upload_dog_photo()


#######################################################
# 5. Obter foto de cachorro
@app.route('/fotoCachorro/<iddog>', methods=['GET'])
def get_dog_photo(iddog=None):
    return upload_routes.get_dog_photo(iddog)


#######################################################
# 6. Deletar foto de perfil
@app.route('/fotoCachorro/<iddog>', methods=['DELETE'])
def delete_dog_photo(iddog=None):
    return upload_routes.delete_dog_photo(iddog)


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
