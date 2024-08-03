CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR,
    book_category VARCHAR
);


CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    review_text VARCHAR,
    like_count INT,
    book_id INT REFERENCES books(book_id)
);

CREATE TABLE fav_text (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR NOT NULL,
    review_text VARCHAR,
    fav BOOLEAN
);

CREATE TABLE evaluated_presentation (
    id SERIAL PRIMARY KEY,
    ai_answer VARCHAR,
    rating INT
);

CREATE INDEX trgm_idx ON books USING gin (title gin_trgm_ops);

COPY books FROM '/data/books.csv' DELIMITER ',' CSV HEADER;

CREATE TEMP TABLE temp_reviews AS
SELECT * FROM reviews LIMIT 0;

COPY temp_reviews FROM '/data/reviews.csv' DELIMITER ',' CSV HEADER;

INSERT INTO reviews
SELECT * FROM temp_reviews
ON CONFLICT (review_id) DO NOTHING;

