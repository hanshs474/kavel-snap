# kavel snap

Generate AI images from the terminal with no API key: `sudo snap install kavel`, then

```bash
kavel "matte black ceramic mug on pale oak, soft window light"
kavel -ratio 16:9 "an isometric coffee shop, pastel palette"
```

It prints a link to the finished image. The binary is the example CLI of
[kavel-go](https://github.com/hanshs474/kavel-go), talking to the free tier of
[Kavel AI](https://www.kavel.ai/?utm_source=snapcraft&utm_medium=package). Set `KAVEL_API_KEY` to a key
from [kavel.ai/settings/apikeys](https://www.kavel.ai/settings/apikeys?utm_source=snapcraft&utm_medium=package)
to run on your account.

`build.sh` cross-compiles the binary for amd64 and arm64 and packs `snap.yaml` with
`mksquashfs`.
