from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SelectField, TextField, DateField, IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired

csrf = CSRFProtect()

class borrowForm(FlaskForm):

    bookname = StringField('BookName', validators=[DataRequired()])
    membername = StringField('Membername', validators=[DataRequired()])
    retcharge = IntegerField('Charges')
    selectaction = SelectField('Action', choices=[('B','Borrow'),('R','return')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class addUser(FlaskForm):
    addname = StringField('User name')
    updatename = StringField('New name')
    addbook = StringField('Book name')
    addcharge = IntegerField('Charges')
    addselect = SelectField('Action', choices=[('C', 'Create'), ('R', 'Read'), ('U', 'Update'),('D', 'Delete')], validators=[DataRequired()])
    addsubmit = SubmitField('Submit')

class addBook(FlaskForm):
    entrybook = StringField('Book Name')
    entryupdate = StringField('New Name')
    entryauthor = StringField('Author name')
    entrystock = IntegerField('Quantity')
    entryselect = SelectField('Action', choices=[('C', 'Create'), ('R', 'Read'), ('U', 'Update'), ('D', 'Delete')],validators=[DataRequired()])
    entrysubmit = SubmitField('Submit')

class report(FlaskForm):
    startdate = DateField("Start Date")
    enddate = DateField("End Date")
    gen = SubmitField('Submit')