from flask import request, redirect
from flask.templating import render_template
from flask.helpers import flash, url_for
from bookfinder.server.services.book_service import BookService
from bookfinder.errors import BookSearcherException
import json
from bookfinder.server.utils.forms import FinderForm
from bookfinder.server.models.book_model import book_info_to_json
from bookfinder.server.app.finder_app import app


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
