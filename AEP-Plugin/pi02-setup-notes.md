# pi02 Setup Notes — Zero 2W

## Current state (2026-04-21)
- Pi is running at **192.168.0.96** on the andeye WiFi (en11 subnet)
- SSH port 22 is open but rejecting all keys — authorized_keys was not written correctly
- Web UI / Pioreactor HTTP interface not responding
- mDNS (`pi02.local`) not resolving — avahi likely hasn't propagated yet

## What was attempted
1. Burned Pioreactor image with hostname `pi02`, username `mcomz`
2. `PasswordAuthentication` is disabled in sshd_config (key-only)
3. Tried adding `firstrun.sh` to the FAT boot partition + `systemd.run=` hook in `cmdline.txt`
4. Script ran (deleted itself) but key was not added — likely `chown mcomz:mcomz` failed because the user didn't exist yet in the minimal `kernel-command-line.target` boot environment

## Recommendation: rebuild from scratch

### In Raspberry Pi Imager — Advanced Options (gear icon)
- Hostname: `pi02`
- Username: `mcomz`
- Password: (set something you'll remember)
- **Enable SSH → "Allow public-key authentication only"**
- Paste in `~/.ssh/id_ed25519.pub` as the authorised key
- WiFi: andeye credentials, GB region

This bakes the key directly into the image via the imager's own firstrun mechanism — much more reliable than post-burn surgery.

## After first boot
```bash
ssh mcomz@pi02.local        # or 192.168.0.96 if mDNS still not working
```

## MAC address of this Pi
`d8:3a:dd:e7:63:cf` — useful if DHCP assigns a different IP after rebuild.

## Claude session
claude --resume 42874354-8948-49cb-80a4-c2d1cb1780bf
