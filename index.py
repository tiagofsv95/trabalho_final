from flask import Flask
from flask import jsonify
from flask import make_response
import os
import breed_routes
import breed_size_routes
import user_routes
import dog_routes
import information_routes

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
# 2. Buscar usuarios todos os usuarios
@app.route('/usuarios', methods=['GET'])
def get_all_users():
    return user_routes.get_all_users()

#######################################################
# 3. Buscar usuario pelo id
@app.route('/usuario/<iduser>', methods=['GET'])
def get_user_by_id(iduser=None):
    return user_routes.get_user_by_id(iduser)

#######################################################
# 4. Atualizar usuarios pelo id
@app.route('/usuario/<iduser>', methods=['PUT'])
def update_user(iduser=None):
    return user_routes.update_user(iduser)

#######################################################
# 5. Deletar usuarios pelo id
@app.route('/usuario/<iduser>', methods=['DELETE'])
def delete_user(iduser=None):
    return user_routes.delete_user(iduser)

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
    return breed_routes.get_breed_by_id(idbreed)

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
    return dog_routes.create_dog()

#######################################################
# 2. Atualizar cachorro
@app.route('/cachorro', methods=['PUT'])
def update_dog():
    return dog_routes.update_dog()

#######################################################
# 3. Deletar cachorro
@app.route('/cachorro/<iddog>', methods=['DELETE'])
def delete_dog(iddog=None):
    return dog_routes.delete_dog(iddog)

#######################################################
# 4. Buscar cachorro pelo id
@app.route('/cachorro/<iddog>', methods=['GET'])
def get_dog_by_id(iddog=None):
    return dog_routes.get_dog_by_id(iddog)

#######################################################
# 5. Buscar cachorro por usuario
@app.route('/usuarioCachorros/<iduser>', methods=['GET'])
def get_dogs_by_user(iduser=None):
    return dog_routes.get_dogs_by_user(iduser)

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