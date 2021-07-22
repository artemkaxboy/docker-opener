# Must have linux/arm/v7 manifest
FROM busybox:1.33.1 as busybox
# -----------------------------

# Must have linux/arm/v7 manifest
FROM docker:19.03

ARG VERSION=SNAPSHOT
ARG REVISION
ARG REF_NAME

# https://github.com/opencontainers/image-spec/blob/main/annotations.md

# LABEL org.opencontainers.image.created=
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

COPY --from=busybox /bin/busybox /busybox
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
