#!/usr/bin/env python3

import json
import sys

from datetime import datetime
from subprocess import run
from urllib.request import urlopen

VERSIONS_IMAGE = "docker.io/almalinux"
ATOMIC_IMAGE_REGISTRY = "quay.io"
ATOMIC_IMAGE_REPO = "almalinuxorg/almalinux-bootc"

def err(msg):
    print(msg, file=sys.stderr)

if len(sys.argv) != 2:
    err("Usage: get_build_matrix.py <output_image>")
    sys.exit(1)

output_image = sys.argv[1]

result = run(["skopeo", "--version"], check=False, capture_output=True)
if result.returncode != 0:
    err("skopeo is not available")
    sys.exit(1)

# The official docker image is uses to list versions on the assumption it will be a more reliable indicator
# of what has actually been released as stable
result = run(
    ["skopeo", "list-tags", f"docker://{VERSIONS_IMAGE}"],
    capture_output=True, text=True, check=True
)
tags = json.loads(result.stdout)["Tags"]
whole_number_tags = sorted([tag for tag in tags if tag.isdigit()], reverse=True)
if len(whole_number_tags) == 0:
    err("No whole number tags found")
    sys.exit(1)
latest = int(whole_number_tags[0])

err(f"The latest release is {latest}")

testing = str(latest + 1)
versions = whole_number_tags[:] + [testing]
archs = ["arm64", "amd64"]

err(f"Checking for versions ({' '.join(map(str, versions))}) on archs ({' '.join(archs)})")

today = datetime.now().strftime("%Y%m%d")

output = {
    "images": [],
    "manifests": []
}

for version in versions:

    for arch in archs:
        err(f"Checking {version}/{arch}")

        result = run(
            ["skopeo", "inspect", f"docker://{ATOMIC_IMAGE_REGISTRY}/{ATOMIC_IMAGE_REPO}:{version}", "--override-os", "linux", "--override-arch", arch], 
            capture_output=True, text=True
        )

        if result.returncode != 0:
            continue

        manifest = json.loads(result.stdout)

        available_arch = manifest["Architecture"]
        if available_arch != arch:
            continue

        tags = [str(version), f"{version}.{today}"]

        if version == latest:
            tags.extend(["latest", f"latest.{today}"])
        if version == testing:
            tags.extend(["testing", f"testing.{today}"])

        runner = "ubuntu-24.04"
        if arch == "arm64":
            runner += "-arm"
            
        image = {
            "version_tag": f"{version}.{today}-{arch}",
            "tags": ",".join(map(lambda t: f"{output_image}:{t}-{arch}", tags)),
            "runner": runner,
            "image_base": f"{ATOMIC_IMAGE_REGISTRY}/{ATOMIC_IMAGE_REPO}",
            "image_tag": version
        }
        output["images"].append(image)

        for tag in tags:
            manifest_tag = f"{output_image}:{tag}"
            manifest = next((m for m in output["manifests"] if m["tag"] == manifest_tag), None)
            if manifest is None:
                manifest = {
                    "tag": manifest_tag,
                    "images": []
                }
                output["manifests"].append(manifest)
            manifest["images"].append(f"{output_image}:{tag}-{arch}")

for manifest in output["manifests"]:
    manifest["images"] = " ".join(manifest["images"])

print(json.dumps(output))
