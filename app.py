from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/books_list')
def books_list():
    return render_template("books_list.html")


@app.route('/add_books')
def add_books():
    return render_template("add_books.html")


@app.route('/edit_book')
def edit_book():
    return render_template("edit_book.html")


if __name__ == '__main__':
    app.run()
