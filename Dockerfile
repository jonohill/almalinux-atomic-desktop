ARG IMAGE_BASE=quay.io/almalinuxorg/almalinux-bootc

# This points to the very latest
# It's mainly here to cause rebuilds when renovate updates it
ARG IMAGE_TAG=10@sha256:a06b0198576d9d314f59dcb6cdcc7f9f418b90d5b9bd003fa7274036cf57eff3

FROM ${IMAGE_BASE}:${IMAGE_TAG}

RUN dnf groupinstall -y "Server with GUI"

COPY --chown=root:root root/etc /etc

RUN systemctl --root=/ enable rpm-ostreed-automatic.timer
RUN systemctl --root=/ set-default graphical.target

RUN ostree container commit
