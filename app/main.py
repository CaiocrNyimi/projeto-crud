from flask import Flask, request, jsonify
import psycopg2
import os
import time

for i in range(10):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "usuarios"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "pass")
        )
        break
    except psycopg2.OperationalError:
        print("Aguardando banco de dados iniciar...")
        time.sleep(3)
else:
    print("Não foi possível conectar ao banco.")
    exit(1)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        idade INTEGER,
        email TEXT
    )
''')
conn.commit()

app = Flask(__name__)

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    cursor.execute('INSERT INTO usuarios (nome, idade, email) VALUES (%s, %s, %s)',
                   (data['nome'], data['idade'], data['email']))
    conn.commit()
    return jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    lista = [{'id': u[0], 'nome': u[1], 'idade': u[2], 'email': u[3]} for u in usuarios]
    return jsonify(lista)

@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    data = request.json
    cursor.execute('''
        UPDATE usuarios
        SET nome = %s, idade = %s, email = %s
        WHERE id = %s
    ''', (data['nome'], data['idade'], data['email'], id))
    conn.commit()
    return jsonify({'mensagem': 'Usuário atualizado com sucesso!'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    conn.commit()
    return jsonify({'mensagem': 'Usuário deletado com sucesso!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)