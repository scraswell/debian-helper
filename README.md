# Bootstrapping Bare Metal via Ansible Pull

## Prerequisites

* Arch Linux Live ISO Customized to include with:
  * ansible
  * debootstrap
  * jq
  * git

For general notes see [script](./remastering_cd.sh)

## Beginning the Installation

```sh
ansible-pull -i inventory \
    --url https://github.com/scraswell/debian-helper.git
    -e '{"init":true}'
```

## Customizing the Automated Installation

The automated installation will read the `install_params` kernel parameter from `/proc/cmdline`.  This is expected to be stringified JSON.  Typically, GRUB inputs would be used to construct the `install_params` input.