from flask_wtf.form import Form
from wtforms.fields.core import StringField, RadioField
from wtforms.fields.simple import SubmitField
from wtforms import validators


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
