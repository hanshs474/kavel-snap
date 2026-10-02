"""Log in to the Snap Store with craft-store and push + release both snaps.

  docker run --rm -e UBUNTU_ONE_EMAIL -e UBUNTU_ONE_PASSWORD -e UBUNTU_ONE_OTP \
    -v "$PWD/build:/b" -v "$PWD/upload.py:/upload.py" python:3.12-slim \
    sh -c 'pip install -q craft-store && python /upload.py'
"""
import os, sys, time
from craft_store import UbuntuOneStoreClient, endpoints

client = UbuntuOneStoreClient(
    base_url="https://dashboard.snapcraft.io",
    storage_base_url="https://storage.snapcraftcontent.com",
    auth_url="https://login.ubuntu.com",
    endpoints=endpoints.U1_SNAP_STORE,
    application_name="kavel-upload",
    user_agent="kavel-upload/1",
    environment_auth="SNAPCRAFT_STORE_CREDENTIALS",
    ephemeral=True,
)
kw = dict(email=os.environ["UBUNTU_ONE_EMAIL"], password=os.environ["UBUNTU_ONE_PASSWORD"])
if os.environ.get("UBUNTU_ONE_OTP"):
    kw["otp"] = os.environ["UBUNTU_ONE_OTP"]
client.login(
    permissions=["package_access", "package_push", "package_update", "package_release"],
    description="kavel upload", ttl=3600,
    packages=[endpoints.Package("kavel", "snap")], **kw,
)
print("logged in")

for arch in ("amd64", "arm64"):
    path = f"/b/kavel_0.1.0_{arch}.snap"
    upload_id = client.upload_file(filepath=__import__("pathlib").Path(path))
    r = client.request("POST", "https://dashboard.snapcraft.io/dev/api/snap-push/",
                       json={"name": "kavel", "updown_id": upload_id, "series": "16", "channels": ["stable"]})
    status_url = r.json()["status_details_url"]
    for _ in range(60):
        s = client.request("GET", status_url).json()
        if s.get("processed"):
            print(arch, "revision", s.get("revision"), "errors", s.get("errors"), "released", s.get("channels") or s.get("can_release"))
            break
        time.sleep(5)
    else:
        print(arch, "still processing", s)
