from flask import Flask, jsonify, request, session
from main import app, db


@app.route('/livro', methods=['GET'])
def get_livro():
    livros = Livro.query.all()
    livros_dic = []
    for livro in livros:
        livro_dic = {
            'id_livro': livro.id_livro,
            'titulo': livro.titulo,
            'autor': livro.autor,
            'ano_publicacao': livro.ano_publicacao
        }
        livros_dic.append(livro_dic)
    # retorna dicionario em formato json
    return jsonify(
        mensagem='Lista de Livros',
        livros=livros_dic
    )


@app.route('/livro', methods=['POST'])
def post_livro():
    # pega dados do livro enviado pelo json
    livro = request.json
    # criar nova instancia com base no recebido
    novo_livro = Livro(
        id_livro=livro.get('id_livro'),
        titulo=livro.get('titulo'),
        autor=livro.get('autor'),
        ano_publicacao=livro.get('ano_publicacao')
    )
    # salvar no banco
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify(
        mensagem='Livro Cadastrado com Sucesso',
        livro={
            'id_livro': novo_livro.id_livro,
            'titulo': novo_livro.titulo,
            'autor': novo_livro.autor,
            'ano_publicacao': novo_livro.ano_publicacao
        }
    )


@app.route('/livro/<int:id_livro>', methods=['PUT'])
def put_livro(id_livro):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém o livro pelo ID fornecido
        livro = Livro.query.get(id_livro)
        if livro:
            # Atualiza os dados do livro com base nos dados enviados
            data = request.json
            livro.titulo = data.get('titulo', livro.titulo)
            livro.autor = data.get('autor', livro.autor)
            livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)
            # Salva as mudanças no banco de dados
            db.session.commit()
            return jsonify(
                mensagem='Livro atualizado com sucesso',
                livro={
                    'id_livro': livro.id_livro,
                    'titulo': livro.titulo,
                    'autor': livro.autor,
                    'ano_publicacao': livro.ano_publicacao
                }
            )
        else:
            return jsonify({'mensagem': 'Livro não encontrado'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})


@app.route('/livro/<int:id_livro>', methods=['DELETE'])
def delete_livro(id_livro):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém o livro pelo ID fornecido
        livro = Livro.query.get(id_livro)
        if livro:
            # Remove o livro do banco de dados
            db.session.delete(livro)
            db.session.commit()
            return jsonify({'mensagem': 'Livro excluído com sucesso'})
        else:
            return jsonify({'mensagem': 'Livro não encontrado'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})


from models import Livro, Usuario


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    # Consulta o usuário no banco de dados pelo email fornecido
    usuarios = Usuario.query.filter_by(email=email).first()
    # Verifica se o e-mail está cadastrado e se a senha está correta
    if usuarios and usuarios.senha == senha:
        # Salva o email do usuário na sessão
        session['id_usuario'] = usuarios.id_usuario
        return jsonify({'mensagem': 'Login com sucesso'}), 200
    else:
        # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
        return jsonify({'mensagem': 'Email ou senha inválido'})


@app.route('/protected', methods=['GET'])
def protected():
    # Verifica se o usuário está autenticado verificando se o email está na sessão
    if 'id_usuario' in session:
        return jsonify({'mensagem': 'Rota Protegida'})
    else:
        # Se o usuário não estiver autenticado, retorna uma mensagem de erro
        return jsonify({'mensagem': 'Requer Autorização'})


# Rota para fazer logout
@app.route('/logout', methods=['POST'])
def logout():
    # Remove o email da sessão, efetivamente fazendo logout
    session.pop('id_usuario', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'})