FROM python:3.6.2-alpine3.6

# Build system will provide arguments to identify source location/version
ARG GIT_REPO_NAME='NOT SPECIFIED'
ARG GIT_BRANCH_NAME='NOT SPECIFIED'
ARG GIT_COMMIT_HASH='NOT SPECIFIED'
ARG BUILD_TIMESTAMP='NOT SPECIFIED'

# Label image with source location/version
LABEL com.makara.build.repo=${GIT_REPO_NAME} \
      com.makara.build.branch=${GIT_BRANCH_NAME} \
      com.makara.build.timestamp=${BUILD_TIMESTAMP} \
      com.makara.build.commit-hash=${GIT_COMMIT_HASH}

COPY app/ /app/
COPY requirements.txt /app/
COPY constraints.txt /app/
COPY docker/docker-entrypoint.sh /docker-entrypoint.sh

RUN apk add --no-cache bash && \
    pip install -r /app/requirements.txt

EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh"]