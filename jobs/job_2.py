#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  job_configure-users
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

""" Create KaOS specific settings for users """

from helpers import *
import os
import shutil

def job_configure_users(self, user):
  self.msg_job_start('job_configure-users')

  msg('create common dirs')
  common_dirs = [
                     'Desktop',
                     '.kde4/autostart', 
                     '.kde4/env', 
                     '.kde4/share/config', 
                     '.kde4/share/apps/konqueror', 
                     '.kde4/share/apps/homerun', 
                     '.local/share/applications', 
                     '.kde4/share/kde4/services/searchproviders'
  ]
  for d in common_dirs:
    self.chroot(['/usr/bin/mkdir', '-p', '/home/%s/%s' % (user,  d)])

  msg('setup KaOS settings')
  kaos_settings = [
                    ('kdesplashrc'                 , '.kde4/share/config/'), 
                    ('kcminputrc'                  , '.kde4/share/config/'), 
                    ('kwinrc'                      , '.kde4/share/config/'), 
                    ('plasma-desktop-appletsrc'    , '.kde4/share/config/'), 
                    ('plasmarc'                    , '.kde4/share/config/'), 
                    ('kcmfonts'                    , '.kde4/share/config/'), 
                    ('bookmarks.xml'               , '.kde4/share/apps/konqueror/'), 
                    ('favoriteapps.xml'            , '.kde4/share/apps/homerun/'), 
                    ('rekonqrc'                    , '.kde4/share/config/'), 
                    ('kuriikwsfilterrc'            , '.kde4/share/config/'), 
                    ('kdeglobals'                  , '.kde4/share/config/'), 
                    ('oxygenrc'                    , '.kde4/share/config/'), 
                    ('yakuakerc'                   , '.kde4/share/config/'), 
                    ('kickoffrc'                   , '.kde4/share/config/'), 
                    ('.bashrc'                     , ''), 
                    ('mimeapps.list'               , '.local/share/applications/'), 
                    ('networkmanagementrc'         , '.kde4/share/config/'), 
                    ('duckduckgo.desktop'          , '.kde4/share/kde4/services/searchproviders/'), 
                    ('xdg-user-dirs-update.desktop', '.config/autostart/'), 
                    ('katerc'                      , '.kde4/share/config/')
  ]
  
  for f,  d in kaos_settings:
      shutil.copy2('/etc/skel/%s' % f,  '%s/home/%s/%s%s' % (self.dest_dir,  user,  d,  f))
  
  msg('configure kdmrc')
  kdmrcPath = os.path.join(self.dest_dir, "usr/share/config/kdm/kdmrc")
  if os.path.exists(kdmrcPath):
    os.system("sed -i -e 's~^.*Theme=/.*~Theme=/usr/share/apps/kdm/themes/midna~' %s" % kdmrcPath)
    os.system("sed -i -e 's~^.*#AntiAliasing=.*~AntiAliasing=true~' %s" % kdmrcPath)
    os.system("sed -i -e 's~^.*#TerminateServer=.*~TerminateServer=true~' %s" % kdmrcPath)
    os.system("sed -i -e 's~^.*#HaltCmd=.*~HaltCmd=/sbin/poweroff~' %s" % kdmrcPath)
    os.system("sed -i -e 's~^.*#RebootCmd=.*~RebootCmd=/sbin/reboot~' %s" % kdmrcPath)
  
  self.msg_job_done('job_configure-users')
