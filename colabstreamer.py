import apt, apt.debfile
import pathlib, stat, shutil, urllib.request, subprocess, getpass, time
import secrets, json, re
import IPython.utils.io
import os 

os.environ['DISPLAY'] = ":0"
envc = os.environ.copy()

def _installPkg(cache, name):
  pkg = cache[name]
  if pkg.is_installed:
    print(f"{name} is already installed")
  else:
    print(f"Will Install {name}")
    pkg.mark_install()

def _installPkgs(cache, package_list):
  for p in package_list:
    _installPkg(cache, p)

def _download(url, path):
  try:
    with urllib.request.urlopen(url) as response:
      with open(path, 'wb') as outfile:
        shutil.copyfileobj(response, outfile)
  except:
    print("Failed to download ", url)
    raise

def _install_everything():
  all_packages = ["xvfb", "xserver-xorg", "mesa-utils", "xinit", "xdotool",
                "linux-generic", "xterm", "htop", "i3", "xloadimage"]

  cache = apt.Cache()
  cache.update()
  cache.open(None)
  # cache.upgrade()
  cache.commit()

  _installPkgs(cache, all_packages)

  cache.commit()

def _config_xorg():
  _download("http://us.download.nvidia.com/tesla/418.67/NVIDIA-Linux-x86_64-418.67.run", "nvidia.run")
  pathlib.Path("nvidia.run").chmod(stat.S_IXUSR)
  subprocess.run(["./nvidia.run", "--no-kernel-module", "--ui=none"], input = "1\n", check = True, universal_newlines = True)

  subprocess.run(["nvidia-xconfig",
                  "-a",
                  "--allow-empty-initial-configuration",
                  "--virtual=1920x1080",
                  "--busid", "PCI:0:4:0"],
                  check = True)

  with open("/etc/X11/xorg.conf", "r") as f:
    conf = f.read()
    conf = re.sub('(Section "Device".*?)(EndSection)',
                  '\\1    MatchSeat      "seat-1"\n\\2',
                  conf,
                  1,
                  re.DOTALL)
  with open("/etc/X11/xorg.conf", "w") as f:
    f.write(conf)


def _config_i3():
  _download("https://gist.githubusercontent.com/taesiri/ea3f5c6154ebd31e0c2092606a236a22/raw/6f2314ea55704c6c940aa1a4f8eb89a9a5453577/config", "i3.conf")
  os.makedirs('/root/.config/i3/', exist_ok=True)
  shutil.move("i3.conf", "/root/.config/i3/config")

def config_all():
  _install_everything()
  _config_xorg()
  _config_i3()


def _twitch_stream(stream_secret):
  _xorg = subprocess.Popen(["Xorg", "-seat", "seat-1", "-allowMouseOpenFail", "-novtswitch", "-nolisten", "tcp"])
  _i3 = subprocess.Popen("i3", env=envc, shell=True)
  _ffmpeg = subprocess.Popen(["ffmpeg", "-threads:v", "2", "-threads:a", "8", "-filter_threads", "2", "-thread_queue_size", 
                              "512", "-f", "x11grab", "-s", "1920x1080", "-framerate", "30", "-i", ":0.0", "-b:v", "2400k", 
                              "-minrate:v", "2400k", "-maxrate:v", "2400k", "-bufsize:v", "2400k", "-c:v", "h264_nvenc", 
                              "-qp:v", "19", "-profile:v", "high", "-rc:v", "cbr_ld_hq", "-r:v", "60", "-g:v", "120", 
                              "-bf:v", "3", "-refs:v", "16", "-f", "flv", 
                              "rtmp://live.twitch.tv/app/" + stream_secret])
  

  return (_xorg, _i3, _ffmpeg)

def stream_to_twitch(stream_secret):
  return _twitch_stream(stream_secret)