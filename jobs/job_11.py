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

def job_setup_hardware(self, mountpoint, netinst, pkg_overlay):
  self.msg_job_start('job_setup_hardware')

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
    shutil.copy2(f, os.path.join(self.dest_dir, f))

  # setup proprietary drivers, if detected
  msg('setup proprietary drivers')
  if os.path.exists('/tmp/nvidia'):
    msg('nvidia detected')
    msg('removing unneeded packages')
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'libgl'])
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'xf86-video-nouveau'])
    msg('installing driver')
    if netinst:
      self.chroot(['pacman', '-Rdd', '--noconfirm', 'nvidia-utils', 'nvidia'])
    else:
      self.chroot(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-utils-33*'.format(pkg_overlay)])
      self.chroot(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-33*'.format(pkg_overlay)])
  elif os.path.exists('/tmp/nvidia-304xx'):
    msg('nvidia-304xx detected')
    msg('removing unneeded packages')
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'libgl'])
    self.chroot(['pacman', '-Rdd', '--noconfirm', 'xf86-video-nouveau'])
    msg('installing driver')
    if netinst:
      self.chroot(['pacman', '-Rdd', '--noconfirm', 'nvidia-304xx-utils', 'nvidia-304xx'])
    else:
      self.chroot(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-304xx-utils**'.format(pkg_overlay)])
      self.chroot(['pacman', '-Ud', '--force', '--noconfirm', '{}/nvidia-304xx**'.format(pkg_overlay)])

  # fixing alsa
  self.chroot(['alsactl', '-f', '/var/lib/alsa/asound.state', 'store'])

  self.msg_job_done('job_setup_hardware')
