#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  job_setup_hardware
#
#  Copyright 2014 KaOS (http://kaosx.us)
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Setup graphics drivers and sound """

from jobs.helpers import *
import logging
import os
import shutil

from configobj import ConfigObj
conf_file = '/etc/thus.conf'
configuration = ConfigObj(conf_file)

def job_setup_hardware(self):
  msg_job_start('job_setup_hardware')
  self.pkg_overlay= configuration['install']['PKG_OVERLAY']

  # remove any db.lck
  db_lock = os.path.join(self.dest_dir, "var/lib/pacman/db.lck")
  if os.path.exists(db_lock):
      with misc.raised_privileges():
          os.remove(db_lock)
      logging.debug(_("%s deleted"), db_lock)


  # setup alsa volume levels, alsa blacklist for the pc speaker, blacklist for broken realtek nics
  msg('setup alsa config')
  files_to_copy = ['/etc/asound.state', '/etc/modprobe.d/alsa_blacklist.conf', '/etc/modprobe.d/realtek_blacklist.conf']
  for f in files_to_copy:
    if os.path.exists(f):
      #subprocess.check_call(['cp', '-v', '-a', '-f', f, ''.join(mountpoint, f)])
      shutil.copy2(f, os.path.join(self.dest_dir))

  # setup proprietary drivers, if detected
  msg('setup proprietary drivers')
  if os.path.exists('/tmp/nvidia'):
    msg('nvidia detected')
    msg('removing unneeded packages')
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'libgl'])
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'xf86-video-nouveau'])
    msg('installing driver')
    os.system(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-utils-34*'.format(self.pkg_overlay),'--root',self.dest_dir])
    os.system(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-34*'.format(self.pkg_overlay),'--root',self.dest_dir])
  elif os.path.exists('/tmp/nvidia-304xx'):
    msg('nvidia-304xx detected')
    msg('removing unneeded packages')
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'libgl'])
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'xf86-video-nouveau'])
    msg('installing driver')
    os.system(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-304xx-utils**'.format(self.pkg_overlay),'--root',self.dest_dir])
    os.system(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-304xx**'.format(self.pkg_overlay),'--root',self.dest_dir])

  # fixing alsa
  #self.chroot(['alsactl', '-f', '/var/lib/alsa/asound.state', 'store'])
  
  msg_job_done('job_setup_hardware')
