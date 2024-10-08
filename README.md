upda# Developer guid for Prod

### Create github user for using github actions with non-root

#### - Using Hetzner cloud config
After your server is created, monitor the graph and wait for the CPU usage to drop to 0. Once it stabilizes, you can start an SSH session to access your server.
```shell
#cloud-config
users: 
  - name: github
    sudo: [ 'ALL=(ALL) NOPASSWD:ALL' ]
    shell: /bin/bash
    groups: sudo
    ssh_authorized_keys:
      - <public_ssh_key>
    
packages:
  - fail2ban
  - ufw
package_update: true
package_upgrade: true
runcmd:
  - mkdir -p /var/www/todo
  - chown -R github:github /var/www/todo
  - printf "[sshd]\nenabled = true\nbanaction = iptables-multiport" > /etc/fail2ban/jail.local
  - systemctl enable fail2ban
  - ufw allow OpenSSH
  - ufw allow http
  - ufw allow https
  - ufw --force enable
  - sed -i -e '/^\(#\|\)PermitRootLogin/s/^.*$/PermitRootLogin no/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)PasswordAuthentication/s/^.*$/PasswordAuthentication no/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)KbdInteractiveAuthentication/s/^.*$/KbdInteractiveAuthentication no/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)ChallengeResponseAuthentication/s/^.*$/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)MaxAuthTries/s/^.*$/MaxAuthTries 2/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)AllowTcpForwarding/s/^.*$/AllowTcpForwarding no/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)X11Forwarding/s/^.*$/X11Forwarding no/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)AllowAgentForwarding/s/^.*$/AllowAgentForwarding no/' /etc/ssh/sshd_config
  - sed -i -e '/^\(#\|\)AuthorizedKeysFile/s/^.*$/AuthorizedKeysFile .ssh\/authorized_keys/' /etc/ssh/sshd_config
  - sed -i '$a AllowUsers github' /etc/ssh/sshd_config
  - echo "vm.overcommit_memory=1" | sudo tee -a /etc/sysctl.conf
  - sysctl -p
  - reboot

```

#### - Manually

```shell
sudo adduser github
sudo usermod -aG sudo github
```

Open sudoers file

```shell
sudo visudo
```

Add the following line to grant passwordless sudo access to the github user:

```shell
github ALL=(ALL) NOPASSWD:ALL
```

### Initiate DB

```shell
docker exec -it python_app python
```

```python
import sys

sys.path.append('/var/www/todo/db')
from db.init import create_tables

create_tables()
```

### Updating env inside project using docker

```shell
sudo docker compose up -d --no-deps --build web
```

# Run command in windows

cd /d e:/to-do & E:/to-do/.venv/Scripts/activate & uvicorn main:app --reload --port 5000
cd /d e:/dev/to-do & E:/dev/to-do/.venv/Scripts/activate & uvicorn main:app --reload --port 5000

# db initialization

from db.init import *
create_tables()


