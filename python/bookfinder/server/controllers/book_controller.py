from flask import request, abort, redirect
from flask.templating import render_template
from flask.helpers import flash, url_for
from bookfinder.server.services.book_service import BookService
from bookfinder.errors import BookSearcherException,\
    BookSearcherMaxPageException
import json
from bookfinder.server.app.finder_app import app


def page_counter(current_page, max_page):
    '''Utility function to create the book list pagination component'''
    if max_page < 4:
        return range(1, max_page+1)
    if current_page > 2:
        return range(current_page-1, current_page+2)
    if current_page > max_page-2:
        return range(max_page-2, max_page+1)
    return range(1, 4)


@app.route('/books/<int:page>')
def book_list(page):
    '''Show a book list page by page'''
    query_json = request.args.get('query')
    if not query_json:
        abort(404)
    query = json.loads(query_json)
    books_info = request.args.get('books_info')
    if not books_info:
        book_searcher = BookService()
        try:
            books, max_page = book_searcher.serch(query['data'],
                                                  query['type'],
                                                  page)
        except BookSearcherMaxPageException:
            return abort(404)
        except BookSearcherException as e:
            flash(e.message, 'danger')
            return redirect(url_for('finder'))
    else:
        books_info = json.loads(books_info)
        books = books_info['books']
        max_page = books_info['pages']
    if max_page < page:
        abort(404)
    return render_template('book_list.html',
                           books=books,
                           query=query_json,
                           current_page=int(page),
                           max_page=max_page,
                           pages=page_counter(int(page), max_page))


@app.route('/book/<isbn>')
def book(isbn):
    '''Book profile, show all the information of the book with the input ISBN'''
    book_info = request.args.get('book_info')
    if not book_info:
        book_searcher = BookService()
        try:
            book, _ = book_searcher.serch(isbn, 'isbn')
        except BookSearcherException as e:
            flash(e.message, 'danger')
            return redirect(url_for('finder'))
        book = book[0]
    else:
        book = json.loads(book_info)
        try:
            book = book[0]
        except:
            pass
    return render_template('book.html', book=book)
