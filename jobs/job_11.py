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
  subprocess.check_call(['/bin/rm', '-f', '{}/var/lib/pacman/db.lck'.format(mountpoint)])

  # setup alsa volume levels, alsa blacklist for the pc speaker, blacklist for broken realtek nics
  msg('setup alsa config')
  files_to_copy = ['/etc/asound.state', '/etc/modprobe.d/alsa_blacklist.conf', '/etc/modprobe.d/realtek_blacklist.conf']
  for f in files_to_copy:
    if os.path.exists(f):
    subprocess.check_call(['cp', '-v', '-a', '-f', f, ''.join(mountpoint, f)])

  # setup proprietary drivers, if detected
  msg('setup proprietary drivers')
  if os.path.exists('/tmp/nvidia'):
    msg('nvidia detected')
    msg('removing unneeded packages')
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'libgl', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'xf86-video-nouveau', '--noconfirm'])
    msg('installing driver')
    if netinst:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-S', 'nvidia-utils', 'nvidia', '--noconfirm'])
    else:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/nvidia-utils-33*'.format(pkg_overlay), '--noconfirm'])
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/nvidia-33*'.format(pkg_overlay), '--noconfirm'])
  elif os.path.exists('/tmp/nvidia-304xx'):
    msg('nvidia-304xx detected')
    msg('removing unneeded packages')
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'libgl', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'xf86-nouveau', '--noconfirm'])
    msg('installing driver')
    if netinst:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-S', 'nvidia-304xx-utils', 'nvidia-304xx', '--noconfirm'])
    else:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/nvidia-304xx-utils*'.format(pkg_overlay), '--noconfirm'])
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/nvidia-304xx-3*'.format(pkg_overlay), '--noconfirm'])
  elif os.path.exists('/tmp/nvidia-173xx'):
    msg('nvidia-173xx detected')
    msg('removing unneeded packages')
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'libgl', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'nouveau-dri', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'xf86-nv', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'xf86-nouveau', '--noconfirm'])
    msg('installing driver')
    if netinst:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-S', 'nvidia-173xx-utils', 'nvidia-173xx', '--noconfirm'])
    else:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/nvidia-173xx*'.format(pkg_overlay), '--noconfirm'])
  elif os.path.exists('/tmp/catalyst'):
    msg('catalyst detected')
    msg('removing unneeded packages')
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'libgl', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'nouveau-dri', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'xf86-video-ati', '--noconfirm'])
    msg('installing driver')
    if netinst:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-S', 'catalyst', 'catalyst-utils', '--noconfirm'])
    else:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/catalyst-utils*'.format(pkg_overlay), '--noconfirm'])
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/catalyst-1*'.format(pkg_overlay), '--noconfirm'])
  elif os.path.exists('/tmp/catalyst-legacy'):
    msg('catalyst-legacy detected')
    msg('removing unneeded packages')
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'libgl', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'nouveau-dri', '--noconfirm'])
    subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Rdd', 'xf86-video-ati', '--noconfirm'])
    msg('installing driver')
    if netinst:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-S', 'catalyst-legacy', 'catalyst-legacy-utils', '--noconfirm'])
    else:
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/catalyst-legacy-utils*'.format(pkg_overlay), '--noconfirm'])
      subprocess.check_call(['/usr/bin/pacman', '-r', mountpoint, '-Ud', '--force', '{}/catalyst-legacy-1*'.format(pkg_overlay), '--noconfirm'])

  # fixing alsa
  subprocess.check_call(['alsactl', '-f', '{}/var/lib/alsa/asound.state'.format(mountpoint), 'store'])

  self.msg_job_done('job_setup_hardware')
