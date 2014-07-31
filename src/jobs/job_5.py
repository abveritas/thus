#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  job_cleanup_drivers
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

""" Clean up unused drivers """

from jobs.helpers import *
import logging
import os
import shutil
import subprocess 

def get_used_drivers():
  p1 = subprocess.Popen(['inxi', '-G'], stdout=subprocess.PIPE)
  p2 = subprocess.Popen(['grep', 'drivers'], stdin=p1.stdout, stdout=subprocess.PIPE)
  p1.stdout.close()
  out, err = p2.communicate()
  used_drivers = out.decode().split()
  i = used_drivers.index('\x1b[1;34mdrivers:\x1b[0;37m')
   used_drivers = used_drivers[i+1].split(',')
  used_drivers.append('vesa')
  return used_drivers

def get_all_drivers(dest_dir):
  p1 = subprocess.Popen(['pacman', '-r', dest_dir, '-Q'], stdout=subprocess.PIPE)
  p2 = subprocess.Popen(['grep', 'xf86-video'], stdin=p1.stdout, stdout=subprocess.PIPE)
  p1.stdout.close()
  out, err = p2.communicate()
  all_drivers = []
  return [d[11:].split()[0] for d in out.decode().split() if d.find('xf86-video') == 0]

def job_cleanup_drivers(self):
  msg_job_start('job_cleanup_drivers')

  ###########################################################################
  # CLEANUP XORG DRIVERS
  ###########################################################################
  msg('cleaning up video drivers')

  # remove any db.lck
  db_lock = os.path.join(self.dest_dir, "var/lib/pacman/db.lck")
  if os.path.exists(db_lock):
    with misc.raised_privileges():
      os.remove(db_lock)
    logging.debug(_("%s deleted"), db_lock)

  used_drivers = get_used_drivers()
  all_drivers = get_all_drivers(self.dest_dir)

  # display found drivers
  msg('configured driver: {}'.format(used_drivers))
  msg('installed drivers: {}'.format(all_drivers))

  msg('cleanup not used drivers')
  remove_drivers = [d for d in all_drivers if d not in used_drivers]

  if used_drivers:
    for rdriver in remove_drivers:
      self.chroot(['/usr/bin/pacman', '-Rncs', '--noconfirm', 'xf86-video-%s' % (rdriver)])
  else:
    msg('module not found > not removing any free drivers')
    msg('output of lsmod:')
    os.system(['lsmod', '|', 'sort'])
    msg('output of lsmod done')

  msg('video driver removal complete')

  ###########################################################################
  # CLEANUP INPUT DRIVERS
  ###########################################################################
  msg('cleaning up input drivers')

  with open("/var/log/Xorg.0.log", "r") as searchfile:
    for line in searchfile:
      if "synaptics" in line: 
        self.chroot(['pacman', '-Rncs', '--noconfirm', 'xf86-input-synaptics'])
      if "wacom" in line:
        self.chroot(['pacman', '-Rncs', '--noconfirm', 'xf86-input-wacom'])
  searchfile.close()  
  msg_job_done('job_cleanup_drivers')

  msg('input driver removal complete')

  msg_job_done('job_cleanup_drivers')
