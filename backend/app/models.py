from app import db


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    book_category = db.Column(db.String)


class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String)
    like_count = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))


class FavText(db.Model):
    __tablename__ = "fav_text"
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String, nullable=False)
    review_text = db.Column(db.String)
    fav = db.Column(db.Boolean)


class EvaluatedPresentation(db.Model):
    __tablename__ = "evaluated_presentation"
    id = db.Column(db.Integer, primary_key=True)
    ai_answer = db.Column(db.String)
    rating = db.Column(db.Integer)
