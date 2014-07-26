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
  used_drivers = used_drivers[i].split(',')
  used_drivers.append('vesa')
  return used_drivers

def get_all_drivers(dest_dir):
  p1 = subprocess.Popen(['pacman', '-r', 'dest_dir', '-Q'], stdout=subprocess.PIPE)
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

  p = subprocess.Popen("cat /etc/X11/xorg.conf | sed -n '/Section.*.\"InputDevice\"/,/EndSection/p' | grep -v '#' | grep Driver | cut -d '\"' -f 2", stdout=subprocess.PIPE)
  used_idrivers = p.stdout.read().decode().split()
  p = subprocess.Popen('pacman -r {} -Q | grep xf86-input | cut -d "-" -f 3 | cut -d " " -f 1 | grep -v keyboard | grep -v evdev | grep -vw mouse'.format(self.dest_dir), stdout=subprocess.PIPE)
  all_idrivers = p.stdout.read().decode().split()

  #check for synaptics/wacom driver
  p = subprocess.Popen('cat /var/log/Xorg.0.log', stdout=subprocess.PIPE)
  for e in filter(p.stdout.read().decode().split(), ['synaptics', 'wacom']):
    all_idrivers.remove(e)

  for driver in all_idrivers:
    self.chroot(['/usr/bin/pacman', '-Rncs', 'xf86-input-%s' % driver, '--noconfirm'])

  msg('input driver removal complete')

  msg_job_done('job_cleanup_drivers')
