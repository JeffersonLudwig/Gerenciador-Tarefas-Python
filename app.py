from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), default='Geral') # Nova Coluna
    concluida = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tarefas = Tarefa.query.all()
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    conteudo_tarefa = request.form['conteudo']
    categoria_tarefa = request.form['categoria'] # Pega a categoria do HTML
    
    nova_tarefa = Tarefa(conteudo=conteudo_tarefa, categoria=categoria_tarefa)
    
    try:
        db.session.add(nova_tarefa)
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um erro ao adicionar a tarefa'

@app.route('/deletar/<int:id>')
def deletar(id):
    tarefa_para_deletar = Tarefa.query.get_or_404(id)
    try:
        db.session.delete(tarefa_para_deletar)
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um erro ao deletar'

@app.route('/atualizar/<int:id>')
def atualizar(id):
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.concluida = not tarefa.concluida
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um erro ao atualizar'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)