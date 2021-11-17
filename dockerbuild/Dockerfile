FROM busybox:1.33.1 as busybox
# -----------------------------

FROM docker/compose:1.29.2

RUN apk add --no-cache python3 py3-pip
RUN pip3 install docker

COPY --from=busybox /bin/busybox /bbx/busybox
COPY ./python /python
COPY ./entrypoint.sh /entrypoint.sh

ARG VERSION=SNAPSHOT
ARG REVISION=LOCAL
ARG REF_NAME
ARG CREATED

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
LABEL org.opencontainers.image.title="Docker opener"
LABEL org.opencontainers.image.description="Manage your docker containers easily"

ENV VERSION=${VERSION}
ENV REVISION=${REVISION}
ENV CREATED=${CREATED}

ENTRYPOINT ["/entrypoint.sh"]
