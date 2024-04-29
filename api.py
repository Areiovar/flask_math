from flask import Blueprint, jsonify
import sqlite3

api = Blueprint('api', __name__)

@api.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users ORDER BY id')
    users = c.fetchall()
    conn.close()
    user_list = [{'id': user[0], 'surname': user[1], 'name': user[2], 'patronymic': user[3],
                  'birthdate': user[4], 'sex': user[6]} for user in users]
    response = jsonify(user_list)
    response.headers.add('Content-Type', 'application/json')
    return response

@api.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ? ORDER BY id', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        user_dict = {'id': user[0], 'surname': user[1], 'name': user[2], 'patronymic': user[3],
                     'birthdate': user[4], 'sex': user[6], 'about': user[7]}
        response = jsonify(user_dict)
        response.headers.add('Content-Type', 'application/json')
        return response
    else:
        return jsonify({'error': 'User not found'}), 404
