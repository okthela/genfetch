#!/usr/bin/python3
import time
import shutil
import os
import pyfiglet
import cpuinfo
import platform
from decimal import Decimal, ROUND_DOWN
import psutil
from pathlib import Path

cpu_thang = Path("~/.config/genfetch_cpu.info").expanduser()
hostname_check = Path("/etc/hostname")
gpu1 = os.popen("lspci | grep VGA").read().strip()
gpu = gpu1.replace("10:00.0 VGA compatible controller:", "")
label_width = 9
whoami = os.popen("whoami").read().strip()
whoispc = os.popen("cat /etc/hostname").read().strip()
cpu = os.popen("cat ~/.config/cpu.info").read().strip()
cpu_percentage = psutil.cpu_percent()
cores = os.popen("nproc").read().strip()
ram_max1 = psutil.virtual_memory()
ram_max = ram_max1.total / (1024 ** 3)
ram_avaliable = ram_max1.available / (1024 ** 3)
uptime = time.time() - psutil.boot_time()
disks = psutil.disk_partitions()
packages = os.popen("find /var/db/pkg -mindepth 2 -maxdepth 2 -type d | wc -l").read().strip()
shell = os.environ.get("SHELL")
theme = os.popen("gsettings get org.gnome.desktop.interface gtk-theme").read().strip()
term = os.environ.get("TERM")
line = "- "
square = "■"
ram_usage = float(ram_max) - float(ram_avaliable)
black   = os.popen("tput setaf 0").read()
red     = os.popen("tput setaf 1").read()
green   = os.popen("tput setaf 2").read()
yellow  = os.popen("tput setaf 3").read()
blue    = os.popen("tput setaf 4").read()
magenta = os.popen("tput setaf 5").read()
cyan    = os.popen("tput setaf 6").read()
white   = os.popen("tput setaf 7").read()
reset   = os.popen("tput sgr0").read()

if not hostname_check.exists():
    print("Hostname isnt set! (failed to check for /etc/hostname)")
    exit()

if not cpu_thang.exists():
    print("CPU Info doesnt exist, creating it (this avoids long startups)")
    cpu_not_real1 = cpuinfo.get_cpu_info()
    cpu_not_real = cpu_not_real1["brand_raw"]
    os.system(f"touch ~/.config/cpu.info && echo '{cpu_not_real}' >> ~/.config/genfetch_cpu.info")

logo1 = pyfiglet.figlet_format(f"Gentoo Linux")
print(f"{red}{logo1}")
print(f"{red}{line}{red}{'PC 󰍹':<{label_width}} {whoami}@{whoispc}")
print(f"{red}{line}{red}{'CPU ':<{label_width}} {cpu} x {cores}, util: {cpu_percentage}%")
print(f"{red}{line}{red}{'GPU 󰢮':<{label_width}}{gpu}")
print(f"{red}{line}{red}{'Kernel ':<{label_width}} {platform.release()}")
print(f"{red}{line}{red}{'RAM ':<{label_width}} {ram_max:.1f} GiB ({ram_usage:.2f} GiB used)")
print(f"{red}{line}{red}Uptime   {uptime / 3600:.1f} hours")
print(f"{red}{line}{red}{'Storage 󱊟 :':<{label_width}}")
for parts in disks:
    util = psutil.disk_usage(parts.mountpoint)
    print(f"{blue}  * Device  {parts.device} Mountpoint: '{parts.mountpoint}' usage: {util.used / (1024**3):.2f} GiB out of {util.total / (1024**3):.2f} GiB")
print(f"{magenta}{line}{magenta}{'Terminal  ':<{label_width}} {term}")
print(f"{magenta}{line}{magenta}{'Shell ':<{label_width}} {shell}")
print(f"{magenta}{line}{magenta}{'Packages 󰉍 ':<{label_width}} {packages} (portage)")
print(f"{magenta}{line}{magenta}{'Theme ':<{label_width}} {theme}")
print(f"{magenta}{line}{square} {red}{square} {green}{square} {yellow}{square}{reset}")
print(f"{blue}{line}{square} {magenta}{square} {cyan}{square} {white}{square}{reset}")
