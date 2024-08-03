FROM postgres:13

RUN mkdir data

COPY data/reviews.csv data/reviews.csv
COPY data/books.csv data/books.csv

# Install necessary packages for building pgvector
RUN apt-get update && \
    apt-get install -y git build-essential postgresql-server-dev-13

# Clone pgvector repository and install it
RUN cd /tmp && \
    git clone --branch v0.7.3 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install

# Clean up to reduce the image size
RUN apt-get remove -y git build-essential postgresql-server-dev-13 && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/pgvector

# Copy the initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Set the entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]

# Default command
CMD ["postgres"]

