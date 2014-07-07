def msg(self, mesg):
  print(':: BACKEND {}'.format(mesg))
  return

def msg_job_start(self, mesg):
  print(' ')
  print(' ')
  print('>> STARTING JOB {}'.format(mesg))
  return

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
