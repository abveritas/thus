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

def job_remove_packages(self, pkg_overlay):
  self.msg_job_start('job_remove_packages')

  # remove any db.lck
  db_lock = os.path.join(self.dest_dir, "var/lib/pacman/db.lck")
  if os.path.exists(db_lock):
      with misc.raised_privileges():
          os.remove(db_lock)
      logging.debug(_("%s deleted"), db_lock)

  # Remove thus and depends
  if os.path.exists("%s/usr/bin/thus" % self.dest_dir):
      self.queue_event('info', _("Removing installer (packages)"))
      self.chroot(['pacman', '-Rns', '--noconfirm', 'thus'])
            
  # Remove welcome
  if os.path.exists("%s/usr/bin/welcome" % self.dest_dir):
      self.queue_event('info', _("Removing live ISO (packages)"))
      self.chroot(['pacman', '-R', '--noconfirm', 'welcome'])
            
  # Remove hardware detection
  if os.path.exists("%s/etc/kdeos-hwdetect.conf" % self.dest_dir):
      self.queue_event('info', _("Removing live start-up (packages)"))
      self.chroot(['pacman', '-R', '--noconfirm', 'kdeos-hardware-detection'])
            
  # Remove init-live
  if os.path.exists("%s/etc/live" % self.dest_dir):
      self.queue_event('info', _("Removing live configuration (packages)"))
      self.chroot(['pacman', '-R', '--noconfirm', 'init-live'])

  self.msg_job_done('job_remove_packages')
