from flask import Flask, request, redirect
from flask.templating import render_template
from flask_wtf.form import Form
from wtforms.fields.core import StringField, RadioField
from flask.helpers import flash, url_for
from flask_bootstrap import Bootstrap
from wtforms.fields.simple import SubmitField
from bookfinder.server.book_service import BookService
from wtforms import validators
from bookfinder.errors import BookSearcherException
import json


app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')


class FinderForm(Form):
    query = StringField('', [validators.Required()])
    query_type = RadioField('query_type',
                            choices=[('title', 'Title'),
                                     ('isbn', 'ISBN'),
                                     ('author_name', 'Author name'),
                                     ('publisher_name', 'Publisher name')],
                            default='title'
                            )
    submit = SubmitField('Find book')


@app.route('/', methods=['POST', 'GET'])
def finder():
    form = FinderForm(request.form)
    if request.method == 'POST' and form.validate():
        book_searcher = BookService()
        try:
            books_info = book_searcher.serch(form.query.data,
                                             form.query_type.data)
            return redirect(url_for('book_list', books_info=books_info))
        except BookSearcherException as e:
            flash(e.message, 'danger')
    return render_template('finder.html', form=form)


@app.route('/books')
def book_list():
    books_info = request.args.get('books_info')
    books = json.loads(books_info)
    return render_template('book_list.html', books=books)


@app.route('/book/<isbn>')
def book(isbn):
    book_info = request.args.get('book_info')
    if not book_info:
        book_searcher = BookService()
        book_info = book_searcher.serch(isbn, 'isbn')
    book = json.loads(book_info)[0]
    return render_template('book.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
