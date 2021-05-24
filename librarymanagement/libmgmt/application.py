from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from Models.model import *
from forms import *
from settings import app, db
from datetime import date
import json


# csrf.init_app(app)

@app.route('/createbook', methods=['GET', 'POST'])
def create_book():
    form = addBook()
    if form.validate():
        print("valid")
    book_state = form.entryselect.data
    checkbook = BookInfo.query.filter_by(book_name=form.entrybook.data).first()
    if book_state == "C":
        if checkbook:
            print("Failure")
            return render_template("book.html", msgex="Book Already Exist", form=form)
        else:
            data = BookInfo(book_name=form.entrybook.data, book_author=form.entryauthor.data,
                            book_total=form.entrystock.data, book_stock=form.entrystock.data)
            print(data)
            db.session.add(data)
            db.session.commit()
            return render_template("book.html", msgex="Book Register", form=form)
    if book_state == "R":
        if checkbook:
            print(checkbook.book_name)
            msgread = {"Book Name": checkbook.book_name, "Author name": checkbook.book_author,
                       "Total Quantity": checkbook.book_total, "Current Stock": checkbook.book_stock}
            return render_template("book.html", msg=msgread, form=form)
        else:
            return render_template("book.html", invalidread="Invalid Data", form=form)
    if book_state == "U":
        if checkbook:
            if form.entrystock.data:
                checkbook.book_total = form.entrystock.data + checkbook.book_total - checkbook.book_stock
                checkbook.book_stock = form.entrystock.data
            if form.entryupdate.data:
                print("Updating book")
                checkbook.book_name = form.entryupdate.data
            if form.entryauthor.data:
                print("update author")
                checkbook.book_author = form.entryauthor.data
            db.session.commit()
            return render_template("book.html", update="Update success", form=form)
        else:
            return render_template("book.html", update="Invalid Data", form=form)
    if book_state == "D":
        if checkbook:
            db.session.delete(checkbook)
            db.session.commit()
            return render_template("book.html", delete="Record deleted", form=form)
        else:
            return render_template("book.html", delete="Invalid Data", form=form)
    db.session.commit()

    if form.validate_on_submit() == False:
        print("invalid")
        return render_template("book.html", form=form)
    return render_template("book.html", form=form)


@app.route('/createuser', methods=['GET', 'POST'])
def create_member():
    form = addUser()
    member_state = form.addselect.data
    checkmember = MemberInfo.query.filter_by(username=form.addname.data).first()
    print(checkmember)
    if member_state == "C":
        if checkmember:
            # User exist
            return render_template("member.html", msgex="User Already Exist", form=form)
        else:
            data = MemberInfo(username=form.addname.data)
            db.session.add(data)
            db.session.commit()
            return render_template("member.html", msgex="User Created", form=form)
    if member_state == "R":
        if checkmember:
            # user exist
            userread = {"User Name": checkmember.username, "Borrowed Books": checkmember.borrow_book,
                        "Charges": checkmember.charges_pending}
            return render_template("member.html", msg=userread, form=form)
        else:
            # user not exist
            return render_template("member.html", invalidread="Invalid User", form=form)

    if member_state == "U":
        if checkmember:
            print("Updated")
            if form.updatename.data:
                checkmember.username = form.updatename.data
            if form.addcharge.data:
                checkmember.charges_pending = form.addcharge.data
            db.session.commit()
            return render_template("member.html", update="Updated Successfully", form=form)
        else:
            return render_template("member.html", update="Invalid data", form=form)
    if member_state == "D":
        if checkmember:
            print("deleting")
            db.session.delete(checkmember)
            db.session.commit()
            return render_template("member.html", delete="User deleted", form=form)
        else:
            # user not exist
            return render_template("member.html", delete="Invalid User", form=form)
    if form.validate_on_submit() == False:
        return render_template("member.html", form=form)
    return render_template("member.html", form=form)


@app.route('/searcho', methods=['GET','POST'])
def search():
    if request.method == "POST":
        searchdata = request.form.get('search')
        booksearch = BookInfo.query.filter_by(book_name=searchdata).first()
        sendbook = {"Book name": booksearch.book_name, "Book Author": booksearch.book_author,
                    "Total Quantity": booksearch.book_total, "Current stock": booksearch.book_stock,
                    "Number of Borrows": booksearch.book_borrow}
        if booksearch:
            print ("Bookfound")
            return render_template("report.html", searchop=sendbook)
        else:
            authorsearch = BookInfo.query.filter_by(book_author=searchdata).first()
            if authorsearch:
                print("Author found")
                return render_template("report.html", searchop=authorsearch)
            else:
                return render_template("report.html", searchin="Invalid search")
    else:
        return render_template("report.html")
    return render_template("report.html")

@app.route('/repular', methods=['GET','POST'])
def pular():
    if request.method == 'POST':
        popname = BookInfo.query.order_by(BookInfo.book_borrow).first()
        sendpop = {"Book Name": popname.book_name, "Author name": popname.book_author,
                       "Total Quantity": popname.book_total, "Current Stock": popname.book_stock}
        print (popname.book_borrow)
        return render_template("report.html", popular=sendpop)
    if request.method == 'GET':
        return render_template("report.html")

@app.route('/repayer', methods=['GET','POST'])
def payer():
    if request.method == 'POST':
        payname = MemberInfo.query.order_by(MemberInfo.charges_pending.desc()).first()
        if payname:
            sendpay = {"Book name": payname.username, "Pending charges": payname.charges_pending}
            return render_template("report.html", msg=sendpay)
        else:
            return render_template("report.html")
    else:
        return render_template("report.html")

@app.route('/', methods=['GET', 'POST'])
def borrowbook():
    form = borrowForm()
    print(form.bookname.data)
    user_action = form.selectaction.data
    if user_action == "B":
        checkaction = BookInfo.query.filter_by(book_name=form.bookname.data).first()
        if checkaction:
            if checkaction.book_stock > 0:
                # book available
                checkaction.book_stock = checkaction.book_stock - 1
                borrower = MemberInfo.query.filter_by(username=form.membername.data).first()
                if borrower:
                    if borrower.charges_pending > 500:
                        return render_template("home.html", brow="Charges pending above limit", form=form)
                    else:
                        print("bk", borrower.borrow_book)
                        x = (len(borrower.borrow_book))
                        w = borrower.borrow_book
                        w[x + 1] = form.bookname.data
                        print(w)
                        print("book", borrower.borrow_book)
                        borrower.borrow_book = w
                        addtrans = Transaction(book_name=form.bookname.data, borrow_date=date.today(),
                                               member_name=form.membername.data, charges=0)
                        db.session.add(addtrans)
                        db.session.commit()
                        return render_template("home.html", brow="Book assigned to User", form=form)
                else:
                    return render_template("home.html", form=form)
    if user_action == "R":
        checkaction = Transaction.query.filter_by(book_name=form.bookname.data, member_name=form.membername.data,
                                                  return_date=None).first()
        retdata = BookInfo.query.filter_by(book_name=form.bookname.data).first()
        pend = MemberInfo.query.filter_by(username=form.membername.data).first()
        
        if checkaction:
            if retdata:
                checkaction.return_date = date.today()
                checkaction.charges = checkaction.charges + form.retcharge.data
                retdata.book_stock = retdata.book_stock + 1
                retdata.book_borrow = retdata.book_borrow + 1
                pend.charges_pending = pend.charges_pending + form.retcharge.data
                db.session.commit()
            return render_template("home.html", retn="Book returned by User", form=form)
    print(form.bookname.data)
    print(form.errors)
    if form.validate():
        print ("Valid")
    if form.validate_on_submit() == False:
        return render_template('home.html', form=form)
    return redirect('/')


@app.route('/report', methods=['GET','POST'])
def transactrep():
    if request.method == "POST":
        start_date = request.form.get('startdate')
        end_date = request.form.get('enddate')
        report_data = Transaction.query.filter(Transaction.borrow_date.between(start_date,end_date)).all()
        print(type(report_data))
        for da in report_data:
            print (da.book_name)
        return render_template("report.html", rep=report_data)
    else:
        return render_template("report.html")
    return render_template("report.html")


if __name__ == '__main__':
    app.run(debug=True)
