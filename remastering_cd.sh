#!/bin/bash

# mount /work

rm -rf /work/*

pacman -Sy && pacman -S --noconfirm archiso
curl -L -o /work/archlinux-x86_64.iso https://mirror.csclub.uwaterloo.ca/archlinux/iso/latest/archlinux-x86_64.iso
mount -o loop /work/archlinux-x86_64.iso /mnt

mkdir -pv /work{/iso-root,/fs-root}
rsync -a /mnt/ /work/iso-root
umount /mnt

cd /work

# unsquashfs -f -d fs-root iso-root/arch/x86_64/airootfs.sfs
# mount --bind fs-root fs-root
#  
# arch-chroot fs-root
# 
# pacman-key --init && pacman-key --populate
# pacman -Sy && pacman -S --noconfirm ansible git jq debootstrap archiso
# 
# ## stuff
# 
# exit
# umount fs-root
# 
# rm -rf fs-root/var/cache/pacman/pkg/*
# rm -v iso-root/arch/x86_64/airootfs.sfs iso-root/arch/x86_64/airootfs.sha512 iso-root/arch/x86_64/airootfs.sfs.cms.sig
# mksquashfs fs-root iso-root/arch/x86_64/airootfs.sfs -b 1M -comp xz -Xbcj x86 -always-use-fragments
# sha512sum iso-root/arch/x86_64/airootfs.sfs > iso-root/arch/x86_64/airootfs.sfs.sha512
# gpg --detach-sign --armor -o iso-root/arch/x86_64/airootfs.sfs.cms.sig iso-root/arch/x86_64/airootfs.sfs

cp -r /usr/share/archiso/configs/releng /work/releng

# edit packages.x86_64
echo -e "ansible\ngit\njq\ndebootstrap\n" >> releng/packages.x86_64

# change the boot mode to use grub instead of systemd-boot in profiledef.sh
sed -i 's/systemd-boot/grub/g' releng/profiledef.sh

# change the boot configuration for grub
# write releng/grub/grub_include.cfg
# source above && add menu entry

mkarchiso -v -o /work/out /work/releng 
