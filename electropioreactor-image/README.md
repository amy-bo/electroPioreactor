# electroPioreactor OS image

Raspberry Pi OS image based on the official [Pioreactor](https://pioreactor.com) image with the [electroPioreactor plugin](https://github.com/amy-bo/electroPioreactor) pre-installed and configured.

## Flash with Raspberry Pi Imager

1. Open **Raspberry Pi Imager**
2. Click *Choose OS* → scroll to the bottom → *Use custom*
3. Enter the custom URL:

```
https://amy-bo.github.io/electroPioreactor/os-list.json
```

## Hardware connections

| Component | Pioreactor channel |
|-----------|-------------------|
| Electrode pair | LED channel D |
| CO₂ solenoid | PWM channel 4 |

## Build your own image

### With Ansible (existing Pioreactor)

Apply the plugin to a Pi that already runs the Pioreactor image:

```bash
ansible-playbook -i <pi-ip>, -u pioreactor ansible/electropioreactor.yml --ask-pass
```

### With the customisation script (offline image)

Requires a Linux host with `qemu-user-static` installed. Optionally pass a
local path to the plugin checkout to skip the git-clone-inside-chroot:

```bash
sudo apt install qemu-user-static binfmt-support parted util-linux
sudo bash scripts/customize-image.sh \
    pioreactor-base.img electropioreactor.img \
    /path/to/electroPioreactor/AEP-Plugin
```

The base image is from [Pioreactor/CustoPiZer](https://github.com/Pioreactor/CustoPiZer)
releases, asset `pioreactor_leader_worker.zip`.

### With GitHub Actions

Trigger the **Build electroPioreactor OS image** workflow manually from the Actions tab, or push a `v*` tag to trigger an automated release build.

## Repository layout

```
ansible/electropioreactor.yml   — Ansible playbook for existing Pioreactor devices
scripts/customize-image.sh      — Image customisation script (chroot-based)
docs/os-list.json               — Raspberry Pi Imager custom URL endpoint (GitHub Pages)
docs/index.html                 — Landing page
.github/workflows/build-image.yml — CI/CD: build image, publish release, update JSON
```
