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

def job_cleanup_l10n(self, mountpoint, netinst, pkg_overlay):
  self.msg_job_start('job_cleanup_l10n')

  # remove any db.lck
  db_lock = os.path.join(self.dest_dir, "var/lib/pacman/db.lck")
  if os.path.exists(db_lock):
      with misc.raised_privileges():
          os.remove(db_lock)
      logging.debug(_("%s deleted"), db_lock)

  

  self.msg_job_done('job_cleanup_l10n')
