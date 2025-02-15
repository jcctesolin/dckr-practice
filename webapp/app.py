from flask import Flask, render_template, request, redirect, url_for
import redis
import os
import json

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

def populate_db():
    """Popula o Redis com alguns livros de exemplo, caso o banco esteja vazio."""
    if not db.keys('book:*'):  # Verifica se o banco já tem livros cadastrados
        sample_books = [
            {"title": "Dom Casmurro", "author": "Machado de Assis", "year": 1899},
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "O Pequeno Príncipe", "author": "Antoine de Saint-Exupéry", "year": 1943},
            {"title": "Cem Anos de Solidão", "author": "Gabriel García Márquez", "year": 1967},
            {"title": "O Hobbit", "author": "J.R.R. Tolkien", "year": 1937}
        ]
        for book in sample_books:
            book_id = db.incr('book_id')
            db.set(f'book:{book_id}', json.dumps(book))
        print("Banco populado com dados iniciais!")

app = Flask(__name__)
# db = redis.Redis(host='localhost', port=6379, decode_responses=True)
db = redis.Redis(host=redis_host , port=redis_port, decode_responses=True)

# Executa a população antes de iniciar o servidor Flask
populate_db()

# Página inicial com formulário de cadastro
@app.route('/')
def index():
    return render_template('index.html')

# Rota para adicionar livros
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    
    if title and author and year:
        book_id = db.incr('book_id')  # Gera um ID único
        book_data = json.dumps({"title": title, "author": author, "year": year})
        db.set(f'book:{book_id}', book_data)

    return redirect(url_for('list_books'))

# Rota para listar livros
@app.route('/livros')
def list_books():
    keys = db.keys('book:*')
    books = [json.loads(db.get(key)) for key in keys]

    return render_template('livros.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
