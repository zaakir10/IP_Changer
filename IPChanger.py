import os
import platform
import subprocess
import sys
import time

def install_packages():
    distro = subprocess.check_output(["awk", "-F=", "/^NAME/{print $2}", "/etc/os-release"]).decode().strip('"')
    if 'Ubuntu' in distro or 'Debian' in distro:
        os.system('sudo apt-get update')
        os.system('sudo apt-get install -y curl tor')
    elif 'Fedora' in distro or 'CentOS' in distro or 'Red Hat' in distro or 'Amazon Linux' in distro:
        os.system('sudo yum update')
        os.system('sudo yum install -y curl tor')
    elif 'Arch' in distro:
        os.system('sudo pacman -Sy')
        os.system('sudo pacman -S --noconfirm curl tor')
    else:
        print(f"Unsupported distribution: {distro}. Please install curl and tor manually.")
        sys.exit(1)

def get_ip():
    url = "https://checkip.amazonaws.com"
    get_ip = subprocess.check_output(['curl', '-s', '-x', 'socks5h://127.0.0.1:9050', url]).decode().strip()
    ip = get_ip.split('\n')[0]
    return ip

def change_ip():
    print("Reloading tor service")
    os.system('sudo systemctl reload tor.service')
    print(f"\033[34mNew IP address: {get_ip()}\033[0m")

def main():
    if not (os.path.exists('/usr/bin/curl') and os.path.exists('/usr/bin/tor')):
        print("Installing curl and tor")
        install_packages()

    if not subprocess.call(['systemctl', '--quiet', 'is-active', 'tor.service'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        print("Starting tor service")
        os.system('sudo systemctl start tor.service')

    print("""
   ____ ____  __________ _   _ __________   ___ ____        ____ _   _    _    _   _  ____ _____ ____  
  / ___|  _ \|___ /___ /| \ | |___ /___  | |_ _|  _ \      / ___| | | |  / \  | \ | |/ ___| ____|  _ \ 
 | |  _| |_) | |_ \ |_ \|  \| | |_ \  / /   | || |_) |____| |   | |_| | / _ \ |  \| | |  _|  _| | |_) |
 | |_| |  _ < ___) |__) | |\  |___) |/ /    | ||  __/_____| |___|  _  |/ ___ \| |\  | |_| | |___|  _ < 
  \____|_| \_\____/____/|_| \_|____//_/    |___|_|         \____|_| |_/_/   \_\_| \_|\____|_____|_| \_\
                                                                                                       
    """)

    while True:
        interval = input('\033[34mEnter time interval in seconds (type 0 for infinite IP changes): \033[0m')
        times = input('\033[34mEnter number of times to change IP address (type 0 for infinite IP changes): \033[0m')

        if interval == '0' or times == '0':
            print("Starting infinite IP changes")
            while True:
                change_ip()
                interval = str(10 + int(subprocess.check_output(['shuf', '-i', '10-20', '-n', '1']).decode()))
                time.sleep(float(interval))
        else:
            for _ in range(int(times)):
                change_ip()
                time.sleep(float(interval))

if __name__ == "__main__":
    main()
