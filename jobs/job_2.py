def msg(self, mesg):
  print(':: BACKEND {}'.format(mesg))
  return

def msg_job_start(self, mesg):
  print(' ')
  print(' ')
  print('>> STARTING JOB {}'.format(mesg))
  return

def msg_job_done(self, mesg):
  print('>> JOB {} DONE'.format(mesg))
  print(' ')
  print(' ')
  return

def job_configure-users(self, user):
  self.msg_job_start('job_configure-users')

  msg('create common dirs')
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/Desktop' % (self.dest_dir, user)])
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/.kde4/autostart' % (self.dest_dir, user)])
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/.kde4/env' % (self.dest_dir, user)])
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/.kde4/share/config' % (self.dest_dir, user)])
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/.kde4/share/apps/konqueror' % (self.dest_dir, user)])
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/.kde4/share/apps/homerun' % (self.dest_dir, user)])
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/.local/share/applications' % (self.dest_dir, user)])
  subprocess.check_call(['mkdir', '-p', '%s/home/%s/.kde4/share/kde4/services/searchproviders' % (self.dest_dir, user)])

  msg('setup KaOS settings')
  shutil.copy2('/etc/skel/ksplashrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/ksplashrc') % user)
  shutil.copy2('/etc/skel/kcminputrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/kcminputrc') % user)
  shutil.copy2('/etc/skel/kwinrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/kwinrc') % user)
  shutil.copy2('/etc/skel/plasma-desktop-appletsrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/plasma-desktop-appletsrc') % user)
  shutil.copy2('/etc/skel/plasmarc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/plasmarc') % user)
  shutil.copy2('/etc/skel/kcmfonts',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/kcmfonts') % user)
  shutil.copy2('/etc/skel/bookmarks.xml',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/apps/konqueror/bookmarks.xml') % user)
  shutil.copy2('/etc/skel/favoriteapps.xml',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/apps/homerun/favoriteapps.xml') % user)
  shutil.copy2('/etc/skel/rekonqrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/rekonqrc') % user)
  shutil.copy2('/etc/skel/kuriikwsfilterrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/kuriikwsfilterrc') % user)
  shutil.copy2('/etc/skel/kdeglobals',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/kdeglobals') % user)
  shutil.copy2('/etc/skel/oxygenrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/oxygenrc') % user)
  shutil.copy2('/etc/skel/yakuakerc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/yakuakerc') % user)
  shutil.copy2('/etc/skel/kickoffrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/kickoffrc') % user)
  shutil.copy2('/etc/skel/.bashrc',
                 os.path.join(self.dest_dir, 'home/%s/.bashrc') % user)
  shutil.copy2('/etc/skel/mimeapps.list',
                 os.path.join(self.dest_dir, 'home/%s/.local/share/applications/mimeapps.list') % user)
  shutil.copy2('/etc/skel/networkmanagementrc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/networkmanagementrc') % user)
  shutil.copy2('/etc/skel/duckduckgo.desktop',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/kde4/services/searchproviders/duckduckgo.desktop') % user)
  shutil.copy2('/etc/skel/xdg-user-dirs-update.desktop',
                 os.path.join(self.dest_dir, 'home/%s/..config/autostart/xdg-user-dirs-update.desktop') % user)
  shutil.copy2('/etc/skel/katerc',
                 os.path.join(self.dest_dir, 'home/%s/.kde4/share/config/katerc') % user)
  
  msg('configure kdmrc')
  kdmrcPath = os.path.join(self.dest_dir, "usr/share/config/kdm/kdmrc")
  if os.path.exists(kdmrcPath):
  os.system("sed -i -e 's~^.*Theme=/.*~Theme=/usr/share/apps/kdm/themes/midna~' %s" % kdmrcPath)
  os.system("sed -i -e 's~^.*#AntiAliasing=.*~AntiAliasing=true~' %s" % kdmrcPath)
  os.system("sed -i -e 's~^.*#TerminateServer=.*~TerminateServer=true~' %s" % kdmrcPath)
  os.system("sed -i -e 's~^.*#HaltCmd=.*~HaltCmd=/sbin/poweroff~' %s" % kdmrcPath)
  os.system("sed -i -e 's~^.*#RebootCmd=.*~RebootCmd=/sbin/reboot~' %s" % kdmrcPath)
  
  self.msg_job_done('job_configure-users')
