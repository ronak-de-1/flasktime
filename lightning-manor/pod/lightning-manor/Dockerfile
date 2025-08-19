FROM 228121743428.dkr.ecr.eu-west-1.amazonaws.com/iml-base-full:iml-mongodb-full

ENV PYTHONPATH='/opt/'
RUN export DEBIAN_FRONTEND="noninteractive" \
    && apt update || true \
    && apt install -y gnupg wget \
    && rm -f /etc/apt/sources.list.d/mongodb-org-4.4.list \
    && wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | gpg --dearmor > /usr/share/keyrings/mongodb-archive-keyring.gpg \
    && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" > /etc/apt/sources.list.d/mongodb-org-4.4.list \
    && apt update \
    && apt upgrade -yq \
    && apt install -y \
        python3 \
        python3-pip \
    && apt autoremove -yq \
    && apt purge -y gnupg wget \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 27017

RUN pip3 install --no-cache-dir \
    flask \
    gunicorn \
    flask_pymongo \
    pymongo \
    passlib

RUN mkdir -p /data/db 

ENV MONGODB_DATABASE "haunted-hallow"
ENV MONGODB_USER_NAME "jack"
ENV MONGODB_USER_PASSWORD "horseman"

COPY supporting-files/ /