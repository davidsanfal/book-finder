from flask import Flask, request, redirect, abort
from flask.templating import render_template
from flask_wtf.form import Form
from wtforms.fields.core import StringField, RadioField
from flask.helpers import flash, url_for
from flask_bootstrap import Bootstrap
from wtforms.fields.simple import SubmitField
from bookfinder.server.book_service import BookService, book_info_to_json
from wtforms import validators
from bookfinder.errors import BookSearcherException
import json


app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')


class FinderForm(Form):
    query = StringField('', [validators.Required()])
    query_type = RadioField('query_type',
                            choices=[('title', 'Specific title'),
                                     ('all', 'All books'),
                                     ('isbn', 'ISBN'),
                                     ('author_name', 'Author'),
                                     ('publisher_name', 'Publisher'),
                                     ('book_summary', 'Topics')],
                            default='title'
                            )
    submit = SubmitField('Find book')


@app.route('/', methods=['POST', 'GET'])
def finder():
    form = FinderForm(request.form)
    if request.method == 'POST' and form.validate():
        book_searcher = BookService()
        try:
            books_info, pages = book_searcher.serch(form.query.data,
                                                    form.query_type.data)
            if pages:
                books_info = book_info_to_json(books_info)
                query = json.dumps({'data': form.query.data,
                                    'type': form.query_type.data,
                                    'pages': pages})
                return redirect(url_for('book_list',
                                        page=1,
                                        books_info=books_info,
                                        query=query))
            else:
                book = books_info[0]
                return redirect(url_for('book',
                                        isbn=book.isbn10,
                                        book_info=book.to_json))
        except BookSearcherException as e:
            flash(e.message, 'danger')
    return render_template('finder.html', form=form)


def page_counter(current_page, max_page):
    if max_page < 4:
        return range(1, max_page+1)
    if current_page > 2:
        return range(current_page-1, current_page+2)
    if current_page > max_page-2:
        return range(max_page-2, max_page+1)
    return range(1, 4)


@app.route('/books/<page>')
def book_list(page):
    query_json = request.args.get('query')
    if not query_json:
        abort(404)
    query = json.loads(query_json)
    max_page = query['pages']
    books_info = request.args.get('books_info')
    if not books_info:
        book_searcher = BookService()
        books, _ = book_searcher.serch(query['data'],
                                       query['type'],
                                       page)
    else:
        books = json.loads(books_info)
    return render_template('book_list.html',
                           books=books,
                           query=query_json,
                           current_page=int(page),
                           max_page=max_page,
                           pages=page_counter(int(page), max_page))


@app.route('/book/<isbn>')
def book(isbn):
    book = None
    book_info = request.args.get('book_info')
    if not book_info:
        book_searcher = BookService()
        book, _ = book_searcher.serch(isbn, 'isbn')
        book = book[0]
    else:
        book = json.loads(book_info)
        try:
            book = book[0]
        except:
            pass
    return render_template('book.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
