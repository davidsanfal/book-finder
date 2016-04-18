from flask import Flask, request
from flask.templating import render_template
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def searcher():
    if request.method == 'POST':
        pass
    return render_template('search.html')

if __name__ == '__main__':
    app.run()
