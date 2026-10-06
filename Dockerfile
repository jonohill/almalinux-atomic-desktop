ARG IMAGE_BASE=quay.io/almalinuxorg/almalinux-bootc

# This points to the very latest
# It's mainly here to cause rebuilds when renovate updates it
ARG IMAGE_TAG=10@sha256:1bf84d0720dca762a9b1e3cf7143a3dad2b0f85ea7848a3e9405b37472510371

FROM ${IMAGE_BASE}:${IMAGE_TAG}

RUN dnf groupinstall -y "Server with GUI"

COPY --chown=root:root root/etc /etc

RUN systemctl --root=/ enable rpm-ostreed-automatic.timer
RUN systemctl --root=/ set-default graphical.target

RUN ostree container commit
