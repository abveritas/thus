#!/bin/sh
kernel_cmdline ()
{
    for param in $(/bin/cat /proc/cmdline); do
        case "${param}" in
            $1=*) echo "${param##*=}"; return 0 ;;
            $1) return 0 ;;
            *) continue ;;
        esac
    done
    [ -n "${2}" ] && echo "${2}"
    return 1
}

# chroot_mount()
# prepares target system as a chroot
#
chroot_mount()
{
    [[ -e "${DESTDIR}/sys" ]] || mkdir -m 555 "${DESTDIR}/sys"
    [[ -e "${DESTDIR}/proc" ]] || mkdir -m 555 "${DESTDIR}/proc"
    [[ -e "${DESTDIR}/dev" ]] || mkdir "${DESTDIR}/dev"
    mount -t sysfs sysfs "${DESTDIR}/sys"
    mount -t proc proc "${DESTDIR}/proc"
    mount -o bind /dev "${DESTDIR}/dev"
    chmod 555 "${DESTDIR}/sys"
    chmod 555 "${DESTDIR}/proc"
}

# chroot_umount()
# tears down chroot in target system
#
chroot_umount()
{
    umount "${DESTDIR}/proc"
    umount "${DESTDIR}/sys"
    umount "${DESTDIR}/dev"
}

USENONFREE="$(kernel_cmdline nonfree no)"
VIDEO="$(kernel_cmdline xdriver no)"
DESTDIR="/install"

echo "MHWD-Driver: ${USENONFREE}"
echo "MHWD-Video: ${VIDEO}"

chroot_mount

mkdir -p ${DESTDIR}/opt/livecd
mount -o bind /opt/livecd ${DESTDIR}/opt/livecd > /tmp/mount.pkgs.log
ls ${DESTDIR}/opt/livecd >> /tmp/mount.pkgs.log

        # setup proprietary drivers, if detected
	msg "setup proprietary drivers"
	if [ -e "/tmp/nvidia" ] ; then
		msg "nvidia detected"

		msg "removing unneeded packages"
		chroot ${DESTDIR} /usr/bin/pacman -Rdd libgl --noconfirm
		chroot ${DESTDIR} /usr/bin/pacman -Rdd xf86-video-nouveau --noconfirm
        msg "installing driver"
            chroot ${DESTDIR} /usr/bin/pacman -Ud --force /opt/kdeos/pkgs/nvidia-utils-33* --noconfirm
            chroot ${DESTDIR} /usr/bin/pacman -Ud --force /opt/kdeos/pkgs/nvidia-33* --noconfirm
        fi

	elif [ -e "/tmp/nvidia-304xx" ] ; then
		msg "nvidia-304xx detected"

		msg "removing unneeded packages"
		chroot ${DESTDIR}/usr/bin/pacman -Rdd libgl --noconfirm
		chroot ${DESTDIR}/usr/bin/pacman -Rdd xf86-nouveau --noconfirm
		msg "installing driver"
            chroot ${DESTDIR}/usr/bin/pacman -Ud --force /opt/kdeos/pkgs/nvidia-304xx-utils* --noconfirm
            chroot ${DESTDIR}/usr/bin/pacman -Ud --force /opt/kdeos/pkgs/nvidia-304xx-3* --noconfirm
        fi
        #
	# CLEANUP UP LOCALIZATION
	#
	USED_L10N=${kdelang}
	ALL_L10N=$(pacman -r ${DESTDIR} -Q | grep ${KDE_L10N_PREFIX} | cut -d " " -f 1 | awk -F "l10n-" '{print $2}')

	msg "configured localization: ${USED_L10N}"
	msg "installed localization(s): ${ALL_L10N}"

            for l10npkg in ${ALL_L10N}
            do
                    if [ "${l10npkg}" != "$USED_L10N" ] ; then
                            pacman -r ${DESTDIR} -Rddn kde-l10n-${l10npkg} --noconfirm
                    fi
            done

	#
	# CLEANUP UP LOCALIZATION CALLIGRA
	#
	USED_L10N=${kdelang}
	ALL_L10NC=$(pacman -r ${DESTDIR} -Q | grep ${CALLIGRA_L10N_PREFIX} | cut -d " " -f 1 | awk -F "l10n-" '{print $2}')

	msg "configured localization: ${USED_L10N}"
	msg "installed calligra localization(s): ${ALL_L10NC}"

            for l10ncpkg in ${ALL_L10NC}
            do
                    if [ "${l10ncpkg}" != "$USED_L10N" ] ; then
                            pacman -r ${DESTDIR} -Rddn calligra-l10n-${l10ncpkg} --noconfirm
                    fi
            done

	msg "l10n removal complete"

	msg_job_done "job_cleanup_l10n"
	
	USED_MODULES=$(lsmod | cut -d' ' -f1)
	ALL_DRIVERS=$(pacman -r ${mountpoint} -Q | grep xf86-video | cut -d "-" -f 3 | cut -d " " -f 1)

	touch /tmp/used_drivers
	[[ $(echo "$USED_MODULES" | grep "^radeon$") ]]  && echo "ati"     >> /tmp/used_drivers
	[[ $(echo "$USED_MODULES" | grep "^i915$") ]]    && echo "intel"   >> /tmp/used_drivers
	[[ $(echo "$USED_MODULES" | grep "^nvidia$") ]]    && echo "nvidia"   >> /tmp/used_drivers

	for driver in ${ALL_DRIVERS}
	do
		[[ $(echo "$USED_MODULES" | grep "^${driver}$") ]] && echo "${driver}" >> /tmp/used_drivers
	done

	# reload real used drivers
        USED_DRIVERS=$(cat /tmp/used_drivers)

	# display found drivers
	msg "configured driver: ${USED_DRIVERS}"
	msg "installed drivers: ${ALL_DRIVERS}"

	msg "remove used drivers and vesa from remove_drivers list"
	echo "${ALL_DRIVERS}" > /tmp/remove_drivers
	for udriver in ${USED_DRIVERS}
	do
		for driver in ${ALL_DRIVERS}
		do
		if [ "${driver}" = "${udriver}" ] ; then
			sed -i "/${driver}/d" /tmp/remove_drivers
		fi
		done
	done
	sed -i "/vesa/d" /tmp/remove_drivers

	msg "cleanup drivers"
        REMOVE_DRIVERS=$(cat /tmp/remove_drivers)
	if [[ -n "$USED_DRIVERS" ]]; then
		for rdriver in ${REMOVE_DRIVERS}
		do
			chroot ${DESTDIR} /usr/bin/pacman -Rn xf86-video-${rdriver} --noconfirm
		done
		msg "remove any unneeded dri pkgs"
                # tmp fix, use pacman -Rnscu $(pacman -Qdtq) somewhere at the end later
                # grep errors out if it can't find anything > using sed instead of grep, 
                REMOVE_DRI=$(pacman -r ${DESTDIR} -Qdtq | sed -n '/dri/ p')
		for rdri in ${REMOVE_DRI}
		do
			chroot ${DESTDIR} /usr/bin/pacman -Rn ${rdri} --noconfirm
		done
	else
		msg "module not found > not removing any free drivers"
		msg "output of lsmod:"
		lsmod | sort
		msg "output of lsmod done"
	fi

	msg "video driver removal complete"


	###########################################################################
	# CLEANUP INPUT DRIVERS
	###########################################################################
	msg "cleaning up input drivers"

	USED_IDRIVER=`cat /etc/X11/xorg.conf | sed -n '/Section.*."InputDevice"/,/EndSection/p' | grep -v "#" | grep Driver | cut -d '"' -f 2`
	ALL_IDRIVERS=`pacman -r ${DESTDIR} -Q | grep xf86-input | cut -d "-" -f 3 | cut -d " " -f 1 | grep -v keyboard | grep -v evdev | grep -vw mouse`

	for i in $USED_IDRIVER
	do
		if [ "${i}" = "acecad" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "aiptek" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "calcomp" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "citron" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "digitaledge" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "dmc" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "dynapro" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "elo2300" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "elographics" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "fpit" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "hyperpen" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "jamstudio" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "joystick" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "magellan" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "magictouch" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "microtouch" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "mutouch" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "palmax" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "penmount" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "spaceorb" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "summa" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "evdev" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "tek4957" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "ur98" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "vmmouse" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		elif [ "${i}" = "void" ] ; then
			ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"${i}"/""/g`

		fi
	done

	#check for synaptics driver
	if cat /var/log/Xorg.0.log | grep "synaptics" > 0 ; then
		ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"synaptics"/""/g`
	fi
	
	#check for wacom driver
	if cat /var/log/Xorg.0.log | grep "wacom" > 0 ; then
		ALL_IDRIVERS=`echo $ALL_IDRIVERS | sed s/"wacom"/""/g`
	fi

	for driver in ${ALL_IDRIVERS}
	do
		chroot ${DESTDIR} /usr/bin/pacman -Rncs xf86-input-${driver} --noconfirm
	done
	
	msg "input driver removal complete"

	msg_job_done "job_cleanup_drivers"
	
umount ${DESTDIR}/opt/livecd
rmdir ${DESTDIR}/opt/livecd

chroot_umount


