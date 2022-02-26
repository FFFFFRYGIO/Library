from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, flash, session

from manage_books import get_books, add_books as add, edit_book as edit, get_book_by_isbn

app = Flask(__name__)
app.secret_key = '12345'
app.permanent_session_lifetime = timedelta(minutes=10)


@app.route('/', methods=["POST", "GET"])
def home():
    if 'user' in session and len(session['user']):
        if request.method == "POST":
            if session['user'] == request.form['name'] or len(request.form['name']) == 0:
                flash('No changes in session')
            else:
                session.permanent = True
                session.pop('user')
                session['user'] = request.form['name']
                flash('Session changed')
        return render_template("index.html", user=session['user'])
    else:
        if request.method == "POST":
            if len(request.form['name']):
                session.permanent = True
                session['user'] = request.form['name']
                flash('Session created')
                return render_template("index.html", user=session['user'])
            else:
                flash('No name input')
                return render_template("index.html", user='')
        else:
            return render_template("index.html", user='')


@app.route('/books_list', methods=["POST", "GET"])
def books_list():
    if 'user' in session:
        if request.method == "POST":
            book_isbn = request.form['ISBN']
            book_dict = get_book_by_isbn(book_isbn)
            return redirect(url_for("edit_book", book_isbn=book_isbn, book=book_dict, user=session['user']))
        else:
            return render_template("books_list.html", books=get_books(), user=session['user'])
    else:
        flash('No session found')
        return redirect(url_for('home'))


@app.route('/add_books', methods=["POST", "GET"])
def add_books():
    if 'user' in session:
        key_words = {
            'intitle': 'In the title',
            'inauthor': 'In the authors',
            'inpublisher': 'In the publisher',
            'subject': 'In the category list',
            'isbn': 'Exact ISBN number',
            'lccn': 'In the Library of Congress Control Number',
            'oclc': 'In the Online Computer Library Center number',
        }
        if request.method == "POST":
            book_params = {}
            for key in key_words:
                if request.form[key]:
                    book_params[key] = request.form[key]
            count_errors = add(book_params)  # to flash
            if count_errors[0] != -1:
                if count_errors[2]:
                    flash('Adding succesful with ' + str(count_errors[2]) + ' successes')
                else:
                    flash('No books added')
                if count_errors[0]:
                    flash('Errors with lack of ISBN number: ' + str(count_errors[0]))
                if count_errors[1]:
                    flash('Errors with duplicated books: ' + str(count_errors[1]))
            return redirect(url_for("books_list"))
        else:
            return render_template("add_books.html", key_words=key_words, user=session['user'])
    else:
        flash('No session found')
        return redirect(url_for('home'))


@app.route('/edit_book', methods=["POST", "GET"])
def edit_book():
    if 'user' in session:
        if request.method == "POST":
            book_isbn = request.args['book_isbn']
            book_dict = get_book_by_isbn(book_isbn)
            book_dict.pop('ISBN')
            book_config = {}
            for attr in book_dict:
                if book_dict[attr] != request.form[attr]:
                    book_config[attr] = request.form[attr]
            if edit(book_isbn, book_config):
                flash('Successfully modified book with ISBN number ' + book_isbn)
            return redirect(url_for("books_list", user=session['user']))
        else:
            book_isbn = request.args['book_isbn']
            book_dict = get_book_by_isbn(book_isbn)
            book_dict.pop('ISBN')
            return render_template("edit_book.html", book_isbn=book_isbn, book=book_dict, user=session['user'])
    else:
        flash('No session found')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
