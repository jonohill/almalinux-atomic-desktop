ARG IMAGE_BASE=quay.io/almalinuxorg/almalinux-bootc

# This points to the very latest
# It's mainly here to cause rebuilds when renovate updates it
ARG IMAGE_TAG=10@sha256:6c8f5d980db9526bf67f59d7ff8b9b1096ec7111522411039c738e4ba8efc62e

FROM ${IMAGE_BASE}:${IMAGE_TAG}

RUN dnf groupinstall -y "Server with GUI"

COPY --chown=root:root root/etc /etc

RUN systemctl --root=/ enable rpm-ostreed-automatic.timer
RUN systemctl --root=/ set-default graphical.target

RUN ostree container commit
