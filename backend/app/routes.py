from flask import request, jsonify
from app import app, db
from sqlalchemy import text
from sentence_transformers import SentenceTransformer
import numpy as np
import uuid
import os
from openai import OpenAI


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the OCapp main page!"})


@app.route("/search_books", methods=["POST"])
def search_books():
    data = request.get_json()
    title = data.get("title")
    page = data.get("page", 1)
    per_page = 10
    if not title:
        return jsonify({"error": "Title is required"}), 400

    request_id = str(uuid.uuid4())

    threshold = 0.05
    query = text("SET pg_trgm.similarity_threshold = :threshold")
    result = db.session.execute(query, {"threshold": threshold})

    query = text(
        "SELECT book_id, title FROM books WHERE title % :title ORDER BY similarity(title, :title) DESC LIMIT :limit OFFSET :offset"
    )
    offset = (page - 1) * per_page
    result = db.session.execute(
        query, {"title": title, "limit": per_page, "offset": offset}
    )
    books = [{"book_id": row[0], "title": row[1]} for row in result]

    count_query = text("SELECT COUNT(*) FROM books WHERE title % :title")
    count_result = db.session.execute(count_query, {"title": title})
    total_books = count_result.scalar()
    total_pages = (total_books + per_page - 1) // per_page

    return jsonify(
        {"books": books, "request_id": request_id, "totalPages": total_pages}
    )


@app.route("/submit_evaluation", methods=["POST"])
def submit_evaluation():
    data = request.get_json()
    request_id = data.get("request_id")
    book_id = data.get("book_id")
    selected_texts = data.get("selected_texts")
    non_selected_texts = data.get("non_selected_texts")
    num_fetch = data.get("num_fetch")

    if not request_id or not book_id:
        return (
            jsonify({"error": "Request ID, selected texts, and book ID are required"}),
            400,
        )

    if selected_texts or non_selected_texts:
        for selected_text in selected_texts:
            db.session.execute(
                text(
                    "INSERT INTO fav_text (request_id, review_text, fav) VALUES (:request_id, :review_text, true)"
                ),
                {"request_id": request_id, "review_text": selected_text},
            )

        for non_selected_text in non_selected_texts:
            db.session.execute(
                text(
                    "INSERT INTO fav_text (request_id, review_text, fav) VALUES (:request_id, :review_text, false)"
                ),
                {"request_id": request_id, "review_text": non_selected_text},
            )

        db.session.commit()

    count_query = text(
        "SELECT COUNT(*) FROM fav_text WHERE request_id = :request_id AND fav = true"
    )
    count_result = db.session.execute(count_query, {"request_id": request_id}).scalar()

    if count_result < 5:
        is_review_query = text("SELECT COUNT(*) FROM reviews WHERE book_id = :book_id")
        if db.session.execute(is_review_query, {"book_id": book_id}) == 0:
            return jsonify({"message": "reviews not found"})

        next_review_query = text(
            "SELECT review_text FROM (SELECT review_text, like_count FROM reviews WHERE book_id = :book_id ORDER BY RANDOM() LIMIT 10) subquery ORDER BY like_count DESC LIMIT 1 OFFSET :offset"
        )
        result = db.session.execute(
            next_review_query, {"book_id": book_id, "offset": num_fetch}
        )

        if result:
            reviews = []
            for row in result:
                review_text = row[0]
                review_texts = []

                # "." と "。" で分割
                for sentence in review_text.split("."):
                    review_texts.extend(sentence.split("。"))

                # 空の文を除外
                review_texts = [
                    sentence.strip() for sentence in review_texts if sentence.strip()
                ]

                reviews.append(
                    {
                        "review_texts": review_texts,
                    }
                )

            return jsonify({"reviews": reviews})
        else:
            return jsonify({"message": "No more reviews available"}), 404

    return jsonify({"status": "success"})


@app.route("/calculate_similarity", methods=["POST"])
def calculate_similarity():
    data = request.get_json()
    request_id = data.get("request_id")
    if not request_id:
        return jsonify({"error": "Request ID is required"}), 400

    texts_query = text(
        "SELECT review_text FROM fav_text WHERE fav = true AND request_id = :request_id"
    )
    fav_texts = [
        row[0] for row in db.session.execute(texts_query, {"request_id": request_id})
    ]

    if len(fav_texts) < 5:
        return jsonify({"error": "Not enough texts to calculate similarity"}), 400

    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    embeddings = model.encode(fav_texts).tolist()
    embeddings = [str(embedding).replace(" ", "") for embedding in embeddings]

    recommended_reviews = []
    for embedding in embeddings:
        similarity_query = text(
            "SELECT review_id, review_text, book_id FROM reviews ORDER BY review_vector <=> :embedding DESC LIMIT 1"
        )
        similar_review = db.session.execute(
            similarity_query, {"embedding": embedding}
        ).fetchone()

        if not similar_review:
            continue

        book_id = similar_review.book_id
        book_query = text(
            "SELECT title, book_category FROM books WHERE book_id = :book_id"
        )
        book = db.session.execute(book_query, {"book_id": book_id}).fetchone()
        review = {
            "review_text": similar_review[1],
            "book_id": book_id,
            "book_title": book[0],
            "book_category": book[1],
        }
        recommended_reviews.append(review)

    return jsonify({"recommended_reviews": recommended_reviews})


@app.route("/summarize", methods=["POST"])
def summarize_reviews():
    data = request.get_json()
    book_id = data.get("book_id")
    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400

    meta_query = text("SELECT title, book_category FROM books WHERE book_id = :book_id")
    meta_data = db.session.execute(meta_query, {"book_id": book_id}).fetchone()
    title = meta_data[0]
    book_category = meta_data[1].replace("形式：", "")

    reviews_query = text(
        "SELECT review_text FROM reviews WHERE book_id = :book_id ORDER BY like_count DESC LIMIT 100"
    )
    review_texts = [
        row[0] for row in db.session.execute(reviews_query, {"book_id": book_id})
    ]

    if not review_texts:
        return jsonify({"message": "no reviews", "title": title})

    context = "\n".join(review_texts) + "\n"

    prompt = f"Please review the review text for the book below and output a sentence recommending the book. Please use Japanese and make it in the style of a Japanese thesis.:\n\n{context}\nanswer:"

    # api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    ai_answer = completion.choices[0].message.content
    ai_answers = []

    for sentence in ai_answer.split("."):
        for fragment in sentence.split("。"):
            if fragment.strip():
                ai_answers.append(fragment.strip())

    return jsonify(
        {"ai_answers": ai_answers, "title": title, "book_category": book_category}
    )


@app.route("/submit_rating", methods=["POST"])
def submit_rating():
    data = request.get_json()
    ai_answer = data.get("ai_answer")
    rating = data.get("rating")
    if not ai_answer or not rating:
        return jsonify({"error": "ai_answer and rating is required"}), 400

    try:
        db.session.execute(
            text(
                "INSERT INTO evaluated_presentation (ai_answer, rating) VALUES (:ai_answer, :rating)"
            ),
            {"ai_answer": ai_answer, "rating": rating},
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success"})
