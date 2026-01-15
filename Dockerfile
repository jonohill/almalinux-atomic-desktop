ARG IMAGE_BASE=quay.io/almalinuxorg/almalinux-bootc

# This points to the very latest
# It's mainly here to cause rebuilds when renovate updates it
ARG IMAGE_TAG=10@sha256:6ab7dba9db0c4de719253a68e2a7b17269a0493a81f3a6c8f3308bab791c802a

FROM ${IMAGE_BASE}:${IMAGE_TAG}

RUN dnf groupinstall -y "Server with GUI"

COPY --chown=root:root root/etc /etc

RUN systemctl --root=/ enable rpm-ostreed-automatic.timer
RUN systemctl --root=/ set-default graphical.target

RUN ostree container commit
