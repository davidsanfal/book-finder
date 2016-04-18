from flask import Flask, request
from flask.templating import render_template
from flask_wtf.form import Form
from wtforms.fields.core import StringField
from flask.helpers import flash
from flask_bootstrap import Bootstrap
from wtforms.fields.simple import SubmitField
from booksearcher.server.book_service import BookService


app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')


class SearchForm(Form):
    isbn = StringField('ISBN')
    title = StringField('title')
    author = StringField('author')
    publisher = StringField('publisher')
    submit = SubmitField('Search')

    def is_empty(self):
        if self.title.data or self.author.data or self.isbn.data or self.publisher.data:
            return False
        return True

class BookInfo(object):

    def __init__(self, isbn, title, author, publisher):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher

@app.route('/', methods=['POST', 'GET'])
def searcher():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.is_empty():
            flash('Empty Query', 'danger')
        else:
            book_info = BookInfo(form.isbn.data,
                                 form.title.data,
                                 form.author.data,
                                 form.publisher.data)
            book_searcher = BookService()
            info = book_searcher.serch(book_info)
        
    return render_template('search.html', form=form)

if __name__ == '__main__':
    app.run()
