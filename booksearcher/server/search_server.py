from flask import Flask, request
from flask.templating import render_template
from flask_wtf.form import Form
from wtforms.fields.core import StringField, RadioField
from flask.helpers import flash
from flask_bootstrap import Bootstrap
from wtforms.fields.simple import SubmitField
from booksearcher.server.book_service import BookService
from wtforms import validators
from booksearcher.errors import BookSearcherException


app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')


class SearchForm(Form):
    query = StringField('', [validators.Required()])
    query_type = RadioField('query_type', choices=[('title','Title'),
                                                   ('partial_title','Partial title'),
                                                   ('isbn','ISBN'),
                                                   ('author_name','Author name'),
                                                   ('publisher_name','Publisher name')],
                            default='title'
                            )
    submit = SubmitField('Search')

@app.route('/', methods=['POST', 'GET'])
def searcher():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        book_searcher = BookService()
        try:
            books_info = book_searcher.serch(form.query.data,
                                             form.query_type.data)
            print '*' * 20
            for book in books_info:
                print book.title
                print '*' * 20
        except BookSearcherException as e:
            flash(e.message, 'danger')
        
    return render_template('search.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
