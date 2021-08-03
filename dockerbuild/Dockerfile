FROM busybox:1.33.1 as busybox
# -----------------------------

FROM docker/compose:1.29.2

ARG VERSION=SNAPSHOT
ARG REVISION=LOCAL
ARG REF_NAME
ARG CREATED

RUN apk add --no-cache python3 py3-pip
RUN pip3 install docker

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.created=${CREATED}
LABEL org.opencontainers.image.authors="artemkaxboy@gmail.com"
LABEL org.opencontainers.image.url="https://github.com/artemkaxboy/docker-opener"
LABEL org.opencontainers.image.documentation="https://github.com/artemkaxboy/docker-opener"
LABEL org.opencontainers.image.source="https://github.com/artemkaxboy/docker-opener"
LABEL org.opencontainers.image.version=${VERSION}
LABEL org.opencontainers.image.revision=${REVISION}
LABEL org.opencontainers.image.vendor="artemkaxboy@gmail.com"
LABEL org.opencontainers.image.licenses="Apache 2.0"
LABEL org.opencontainers.image.ref.name=${REF_NAME}
LABEL org.opencontainers.image.title="Any docker container opener"
LABEL org.opencontainers.image.description="Shell-in to any docker container easily"

ENV VERSION=${VERSION}
ENV REVISION=${REVISION}
ENV CREATED=${CREATED}

COPY --from=busybox /bin/busybox /busybox
COPY ./python /python
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
