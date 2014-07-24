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

  used_modules = ['lsmod', '|', 'cut', '-d', "' '", '-f1', '|', 'grep']
  drivers = [('^radeon$', 'ati'), ('^i915$', 'intel'), ('^nvidia$', 'nvidia')]
  p = subprocess.Popen('pacman -r {} -Q | grep xf86-video | cut -d "-" -f 3 | cut -d " " -f 1' % self.dest_dir, shell=True, stdout=subprocess.PIPE)
  all_drivers = p.stdout.read().decode().split()
  with open('/tmp/used_drivers', mode='w') as f:
    for e1, e2 in drivers:
      p = subprocess.Popen(list(used_modules).append(e1), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      if p.stdout.read():
        f.write(e2)
    p = subprocess.Popen(all_drivers, shell=True, stdout=subprocess.PIPE)
    for driver in all_drivers:
      p = subprocess.Popen(list(used_modules).append("^" + driver + "$"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      if p.stdout.read():
        f.write(driver)
  f.close()

  used_drivers = []
  with open('/tmp/used_drivers', mode='r') as f:
    used_drivers = [line for line in f]
  f.close()

  # display found drivers
  msg('configured driver: {}'.format(used_drivers))
  msg('installed drivers: {}'.format(all_drivers))

  msg('remove used drivers and vesa from remove_drivers list')
  with open('/tmp/remove_drivers', mode='w') as f:
    for driver in all_drivers:
      if driver not in used_drivers and driver != 'vesa':
        f.write(driver)
  f.close()

  msg('cleanup drivers')
  remove_drivers = []
  with open('/tmp/remove_drivers', mode='r') as f:
    remove_drivers = [line for line in f]
  f.close()

  if used_drivers:
    for rdriver in remove_drivers:
      self.chroot(['/usr/bin/pacman', '-Rncs', '--noconfirm', 'xf86-video-%s' % (rdriver)])
    msg("remove any unneeded dri pkgs")
    # tmp fix, use pacman -Rnscu $(pacman -Qdtq) somewhere at the end later
    # grep errors out if it can't find anything > using sed instead of grep,
    p = subprocess.Popen(['pacman', '-r', self.dest_dir, '-Qdtq', '|', 'sed', '-n', '"/dri/ p"'], stdout=subprocess.PIPE)
    remove_dri = p.stdout.read().decode().split()
    for rdri in remove_dri:
      os.chroot('/usr/bin/pacman', '-Rn', rdri, '--noconfirm')
  else
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
  filt = [ 'acecad', 'aiptek', 'calcomp', 'citron', 'digitaledge', 'dmc', 'dynapro', 'elo2300', 'elographics',
            'fpit', 'hyperpen', 'jamstudio', 'joystick', 'magellan', 'magictouch', 'microtouch', 'mutouch', 'palmax',
            'penmount', 'spaceorb', 'summa', 'evdev', 'tek4957', 'ur98', 'vmmouse', 'void']
  all_idrivers = [ d for d in all_idrivers if d not in filter(used_idrivers, filt)]

  #check for synaptics/wacom driver
  p = subprocess.Popen('cat /var/log/Xorg.0.log', stdout=subprocess.PIPE)
  for e in filter(p.stdout.read().decode().split(), ['synaptics', 'wacom']):
    all_idrivers.remove(e)

  for driver in all_idrivers:
    self.chroot(['/usr/bin/pacman', '-Rncs', 'xf86-input-%s' % driver, '--noconfirm'])

  msg('input driver removal complete')

  msg_job_done('job_cleanup_drivers')
