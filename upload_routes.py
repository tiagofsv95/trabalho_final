from flask import request, jsonify, make_response, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
from sqlite3 import Error
import os

dirname = os.path.dirname(__file__)
database_dirname = dirname + '/database/adote_um_cao.db'


#######################################################
# 1. Salvar foto de perfil
def upload_profile_photo():
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
                sql = ''' UPDATE Usuario SET foto = ? WHERE id = ''' + '"' + iduser + '"'
                cur = conn.cursor()
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


#######################################################
# 2. Obter foto de perfil
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
            if json_obj['foto']:
                filename = os.path.basename(json_obj['foto'])
                pathname = json_obj['foto'].replace('/'+filename, '')
                return send_from_directory(dirname+pathname, filename)

            else:
                resp = make_response(jsonify({'error': 'Foto do usuario nao encontrado.'}), 404)
                return resp
        else:
            resp = make_response(jsonify({'error': 'Usuario nao encontrado.'}), 400)
            return resp


#######################################################
# 3. Deletar foto de perfil
def delete_profile_photo(iduser=None):
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
            sql = ''' UPDATE Usuario SET foto = NULL WHERE id = ''' + '"' + iduser + '"'
            cur = conn.cursor()
            cur.execute(sql)
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


#######################################################
# 4. Salvar foto de cachorro
def upload_dog_photo():
    iddog = request.args.get('id')
    if not os.path.isdir(dirname+'/uploads/cachorro/'+iddog):
        os.mkdir(dirname+'/uploads/cachorro/'+iddog)
    file = request.files['foto']
    if file.filename == '':
        print('No selected file')
    else:
        try:

            conn = sqlite3.connect(database_dirname)
            sql = '''SELECT * FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
            cur = conn.cursor()
            cur.execute(sql)
            cachorro = cur.fetchone()

            if cachorro:

                filename = secure_filename(file.filename)
                file.save(os.path.join(dirname+'/uploads/cachorro/'+iddog, filename))
                foto = '/uploads/cachorro/'+iddog+'/'+filename
                registro = (foto,)
                sql = ''' UPDATE Cachorro SET foto = ? WHERE id = ''' + '"' + iddog + '"'
                cur = conn.cursor()
                cur.execute(sql, registro)
                conn.commit()

                sql = '''SELECT * FROM Usuario WHERE id = ''' + '"' + iddog + '"'
                cur = conn.cursor()
                cur.execute(sql)
                updated_cachorro = cur.fetchone()

                names = [description[0] for description in cur.description]

                json_obj = dict(zip(names, updated_cachorro))
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
# 5. Obter foto de cachorro
def get_dog_photo(iddog=None):
    if iddog == None:
        resp = make_response(jsonify({'error': 'Parametro id cachorro invalido.'}), 400)
        return resp
    else:
        conn = sqlite3.connect(database_dirname)
        sql = '''SELECT * FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
        cur = conn.cursor()
        cur.execute(sql)
        cachorro = cur.fetchone()

        if cachorro:
            names = [description[0] for description in cur.description]
            json_obj = dict(zip(names, cachorro))
            if json_obj['foto']:
                filename = os.path.basename(json_obj['foto'])
                pathname = json_obj['foto'].replace('/'+filename, '')
                return send_from_directory(dirname+pathname, filename)

            else:
                resp = make_response(jsonify({'error': 'Foto do cachorro nao encontrado.'}), 404)
                return resp
        else:
            resp = make_response(jsonify({'error': 'Cachorro nao encontrado.'}), 400)
            return resp


#######################################################
# 6. Deletar foto de perfil
def delete_dog_photo(iddog=None):
    if iddog == None:
        resp = make_response(jsonify({'error': 'Parametro id cachorro invalido.'}), 400)
        return resp
    else:
        conn = sqlite3.connect(database_dirname)
        sql = '''SELECT * FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
        cur = conn.cursor()
        cur.execute(sql)
        cachorro = cur.fetchone()

        if cachorro:
            sql = ''' UPDATE Cachorro SET foto = NULL WHERE id = ''' + '"' + iddog + '"'
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

            sql = '''SELECT * FROM Cachorro WHERE id = ''' + '"' + iddog + '"'
            cur = conn.cursor()
            cur.execute(sql)
            updated_dog = cur.fetchone()

            names = [description[0] for description in cur.description]

            json_obj = dict(zip(names, updated_dog))
            json_data = [json_obj]

            resp = make_response(jsonify(json_data), 200)
            return resp

        else:
            resp = make_response(jsonify({'error': 'Cachorro nao encontrado.'}), 400)
            return resp
