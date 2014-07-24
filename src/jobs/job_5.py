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
  
  # Drivers to be removed
  self.conflicts = []
  self.running = True
  self.error = False
  self.packages = []

  # remove any db.lck
  db_lock = os.path.join(self.dest_dir, "var/lib/pacman/db.lck")
  if os.path.exists(db_lock):
      with misc.raised_privileges():
          os.remove(db_lock)
      logging.debug(_("%s deleted"), db_lock)
      
  # Cleanup video drivers
  thisVideo= "pacman -Q xf86-video-intel"
  listOfPkgsv= []
  
  p = subprocess.Popen("pacman -Q | grep -i xf86-video | grep -v vesa | awk '{print $1}'", 
      shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  
  # Iterates over every found pkg and put each one in a list
  for line in p.stdout.readlines():
      s = line.decode('ascii')
      s = s.rstrip('\n')
      listOfPkgsv.append(s)
    
  print (listOfPkgsv)
  
  # Remove the pkgs that do not have 'thisVideo'
  for pkg in listOfPkgsv:
      if pkg.find(thisVideo) == -1:
        self.queue_event('info', _("Removing video drivers (packages)"))
        self.chroot(['pacman', '-Rncs', '--noconfirm', 'xf86-video-%s' % (pkg)])

  # Cleanup input drivers 
  searchfile = open("/var/log/Xorg.0.log", "r")
  for line in searchfile:
      if "synaptics" in line is not None: 
        self.chroot(['pacman', '-Rncs', '--noconfirm', 'xf86-input-synaptics'])
  searchfile.close()
  
  searchfile = open("/var/log/Xorg.0.log", "r")
  for line in searchfile:
      if "wacom" in line is not None: 
        self.chroot(['pacman', '-Rncs', '--noconfirm', 'xf86-input-wacom'])
  searchfile.close()

  msg_job_done('job_cleanup_drivers')
