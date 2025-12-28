from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados (SQLite - cria um arquivo local simples)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Tabela no Banco de Dados (Isso é o SQL transformado em Python)
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

# Rota Principal (Mostra as tarefas)
@app.route('/')
def index():
    tarefas = Tarefa.query.all()
    return render_template('index.html', tarefas=tarefas)

# Rota para Adicionar Tarefa
@app.route('/adicionar', methods=['POST'])
def adicionar():
    conteudo_tarefa = request.form['conteudo']
    nova_tarefa = Tarefa(conteudo=conteudo_tarefa)
    
    try:
        db.session.add(nova_tarefa)
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um erro ao adicionar a tarefa'

# Rota para Deletar
@app.route('/deletar/<int:id>')
def deletar(id):
    tarefa_para_deletar = Tarefa.query.get_or_404(id)

    try:
        db.session.delete(tarefa_para_deletar)
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um erro ao deletar'

# Rota para Atualizar (Marcar como feita/não feita)
@app.route('/atualizar/<int:id>')
def atualizar(id):
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.concluida = not tarefa.concluida # Inverte o status
    
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um erro ao atualizar'

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Cria o banco de dados automaticamente se não existir
    app.run(debug=True)