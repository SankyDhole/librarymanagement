from settings import db

class BookInfo(db.Model):
    __tablename__ = 'book_list'
    book_name = db.Column(db.String(100), primary_key=True)
    book_author = db.Column(db.String(100), nullable=False)
    book_total = db.Column(db.Integer, nullable=False)
    book_stock = db.Column(db.Integer, nullable=False)
    book_borrow = db.Column(db.Integer, default=0)

class Transaction(db.Model):
    __tablename__ = 'transaction_list'
    serial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(100), nullable=False)
    borrow_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    member_name = db.Column(db.String(100), nullable=False)
    charges = db.Column(db.Integer)

class MemberInfo(db.Model):
    __tablename__ = 'member_list'
    username = db.Column(db.String(100), primary_key=True)
    borrow_book = db.Column(db.JSON, default=dict)
    charges_pending = db.Column(db.Integer, default=0)

db.create_all()
db.session.commit()


