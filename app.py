from flask import Flask, render_template, request, url_for, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# List of genres available
# Mystery
# Romance
# Thriller
# Drama
# Children


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = "mysecretkey"

app.config['UPLOAD_FOLDER_COVER'] = os.path.join(
    os.path.join(os.getcwd(), "static"), "cover")
app.config['UPLOAD_FOLDER_BOOK'] = os.path.join(
    os.path.join(os.getcwd(), "static"), "pdfs")

db = SQLAlchemy(app)


class User(db.Model):
    emailid = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(1000))
    books = db.relationship("Book", backref="uploaded_books", lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    primary_genre = db.Column(db.String(50))
    secondary_genre = db.Column(db.String(50))
    cover = db.Column(db.String(200))
    book = db.Column(db.String(200))
    uploadDate = db.Column(db.DateTime)
    summary = db.Column(db.String(3000))
    uploadBy = db.Column(db.String(50), db.ForeignKey("user.emailid"))


db.create_all()


@app.route("/", methods=["GET"])
def home():
    if "name" in session.keys():
        print("aaaa")
        return render_template("home.html", authenticated=True)
    else:
        return render_template("home.html", authenticated=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "name" in session.keys():
            return redirect(url_for("viewAll"))
        else:
            return render_template("login.html")
    else:
        emailid = request.form.get("inputEmail")
        password = request.form.get("inputPassword")

        # Getting the email ID
        # SELECT * FROM User WHERE emailid=emailid
        user = User.query.filter_by(emailid=emailid).first()

        if user and check_password_hash(user.password, password):

            session['name'] = user.name
            session['emailid'] = emailid
            return redirect(url_for("home"))

        else:
            flash("Incorrect Credentials")
            return redirect(url_for("login"))


@app.route("/logout", methods=["GET"])
def logout():
    if "name" in session.keys():
        session.pop("name", None)
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if "name" in session.keys():
            return redirect(url_for("viewAll"))
        else:
            return render_template("signup.html")
    else:
        name = request.form.get("inputName")
        emailid = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        retyped = request.form.get("inputRetypedPassword")

        # Checking if the user already exists
        # SELECT * FROM User WHERE emailid=emailid
        user = User.query.filter_by(emailid=emailid).first()

        if user:
            print("User already exists")
            flash("User already exists")
            return redirect("signup")

        if password != retyped:
            print("Passwords don't match")
            flash("Passwords don't match")
            return redirect("signup")

        # INSERT INTO User User VALUES (name, emailid, password)
        new_user = User(name=name,
                        emailid=emailid,
                        password=generate_password_hash(
                            password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        session['name'] = name
        session['emailid'] = emailid

        return redirect(url_for("home"))


@app.route("/book-view", methods=["GET"])
def viewAll():
    if request.method == "GET":
        books = Book.query.all()
        books = books[:21]
        data = []
        row = []
        for index, entry in enumerate(books[::-1]):
            if index % 3 == 0 and index != 0:
                data.append(row)
                row = []
                row.append({"cover": entry.cover,
                            "title": entry.title,
                            "summary": entry.summary[:100],
                            "uploadDate": entry.uploadDate.strftime("%m/%d/%Y"),
                            "id": entry.id
                            })
            else:
                row.append({"cover": entry.cover,
                            "title": entry.title,
                            "summary": entry.summary[:100],
                            "uploadDate": entry.uploadDate.strftime("%m/%d/%Y"),
                            "id": entry.id
                            })

        data.append(row)

        if "name" in session.keys():
            return render_template("viewAll.html", booksList=data, authenticated=True)
        else:
            return render_template("viewAll.html", booksList=data, authenticated=False)


@app.route("/book-view/<int:id>", methods=["GET"])
def viewBook(id):
    book = Book.query.filter_by(id=id).first()
    username = User.query.filter_by(emailid=book.uploadBy).first()

    details = {"title": book.title,
               "author": book.author,
               "primary": book.primary_genre,
               "secondary": book.secondary_genre,
               "cover": book.cover,
               "summary": book.summary,
               "uploadDate": book.uploadDate.strftime("%m/%d/%Y"),
               "book": book.book,
               "uploadBy": username.name
               }
    return render_template("viewOne.html", details=details)


@app.route("/book-upload", methods=["GET", "POST"])
def upload():
    if "name" in session.keys():
        if request.method == "GET":
            return render_template("uploadBook.html")
        else:
            title = request.form.get("title")
            author = request.form.get("authorname")
            primary = request.form.get("primarygenre")
            secondary = request.form.get("secondarygenre")
            summary = request.form.get("summary")
            uploadDate = datetime.utcnow()

            cover = request.files["cover"]
            book = request.files["book"]

            # Checking for the extensions and renaming files
            if cover.filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
                ext = cover.filename.split(".")[-1]
                cover.filename = "_".join(
                    [title, author, "cover", session['name']]) + "." + ext
            else:
                flash(
                    "Cover Image is of incompatible type. Needs to be: PNG, JPEG or JPG")
                return redirect(url_for("upload"))

            if book.filename.split(".")[-1] == "pdf":
                ext = book.filename.split(".")[-1]
                book.filename = "_".join(
                    [title, author, "book", session['name']]) + "." + ext
            else:
                flash("Book is of incompatible type. Needs to be: PDF")
                return redirect(url_for("upload"))

            # For enhanced filtering, the primary and
            # secondary genres should not be same

            if primary == secondary:
                flash("The primary and secondary genres are the same")
                return redirect(url_for("upload"))

            # To ensure integrity, the length of the summary must be less than
            # 500 characters.

            if len(summary) > 3000:
                flash("The summary length is beyond the prescribed limit")
                return redirect(url_for("upload"))

            print(os.path.join(
                app.config["UPLOAD_FOLDER_COVER"], cover.filename))
            cover.save(os.path.join(
                app.config["UPLOAD_FOLDER_COVER"], cover.filename))
            book.save(os.path.join(
                app.config["UPLOAD_FOLDER_BOOK"], book.filename))

            # INSERT INTO Book VALUES (title, author, primary...)
            new_book = Book(title=title,
                            author=author,
                            primary_genre=primary,
                            secondary_genre=secondary,
                            cover=cover.filename,
                            book=book.filename,
                            uploadDate=uploadDate,
                            summary=summary,
                            uploadBy=session['emailid'])

            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("viewAll"))

    else:
        return redirect(url_for("login"))


@app.route("/book-update/<int:id>", methods=["GET", "POST"])
def updateBook(id):
    if "name" in session.keys():
        if request.method == "GET":
            book = Book.query.filter_by(id=id).first()
            details = {"title": book.title,
                       "author": book.author,
                       "cover": book.cover,
                       "summary": book.summary,
                       "id": id
                       }

            return render_template("updateBook.html", details=details)
        else:

            book = Book.query.filter_by(id=id).first()

            book.title = request.form.get('title')
            book.author = request.form.get('authorname')
            book.primary = request.form.get('primarygenre')
            book.secondary = request.form.get('secondarygenre')
            book.summary = request.form.get('summary')

            db.session.commit()

            return redirect(url_for("viewBook", id=id))
    else:
        return redirect(url_for("home"))


@app.route("/book-delete/<int:id>", methods=["GET"])
def deleteBook(id):
    if "name" in session.keys():
        book = Book.query.filter_by(id=id).first()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER_COVER'], book.cover))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER_BOOK'], book.book))
        db.session.delete(book)
        db.session.commit()

        return redirect(url_for("viewAll"))


@app.route('/book-filter/', methods=["POST"])
def filteredView():
    searchitem = request.form.get("search-term").strip(' ')
    genre = request.form.get("search categories")
    final = []

    if genre == "None" and searchitem == '':
        return redirect(url_for("viewAll"))

    elif genre != "None":
        booksPrimary = Book.query.filter_by(primary_genre=genre).all()
        booksSecondary = Book.query.filter_by(secondary_genre=genre).all()
        if searchitem != '':
            for book in booksPrimary:
                if searchitem in book.title or searchitem in book.author:
                    final.append(book)

            for book in booksSecondary:
                if searchitem in book.title or searchitem in book.author:
                    final.append(book)
        else:
            final = booksPrimary + booksSecondary

    else:
        books = Book.query.all()
        if searchitem != "":
            for book in books:
                if searchitem in book.title or searchitem in book.author:
                    final.append(book)

    if len(final) == 0:
        searchresult = "No results found"
    elif genre != "None" and searchitem != "":
        searchresult = f"{len(final)} results found related to {searchitem} by in the genre: {genre}"
    elif searchresult != "":
        searchresult = f"{len(final)} results found related to {searchitem}"
    else:
        searchresult = f"{len(final)} results found in the genre: {genre}"

    data = []
    row = []
    for index, entry in enumerate(final):
        if index % 3 == 0 and index != 0:
            data.append(row)
            row = []
            row.append({"cover": entry.cover,
                        "title": entry.title,
                        "summary": entry.summary[:100],
                        "uploadDate": entry.uploadDate.strftime("%m/%d/%Y"),
                        "id": entry.id
                        })
        else:
            row.append({"cover": entry.cover,
                        "title": entry.title,
                        "summary": entry.summary[:100],
                        "uploadDate": entry.uploadDate.strftime("%m/%d/%Y"),
                        "id": entry.id
                        })

    data.append(row)

    if "name" in session.keys():
        authenticated = True
    else:
        authenticated = False

    return render_template("filtered.html",
                           searchresult=searchresult,
                           booksList=data,
                           authenticated=authenticated
                           )


@app.route('/about-me')
def aboutme():
    return render_template("about.html")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
