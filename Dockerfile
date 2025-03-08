ARG IMAGE_BASE=quay.io/almalinuxorg/almalinux-bootc

# This points to the very latest
# It's mainly here to cause rebuilds when renovate updates it
ARG IMAGE_TAG=9@sha256:0f1b7cca6419eff38c19e17f82d235a3d3bc1828c7af47f524da033b7ef5eae2

FROM ${IMAGE_BASE}:${IMAGE_TAG}

RUN dnf groupinstall -y "Server with GUI"

COPY --chown=root:root root/etc /etc

RUN systemctl --root=/ enable rpm-ostreed-automatic.timer
RUN systemctl --root=/ set-default graphical.target

RUN ostree container commit
