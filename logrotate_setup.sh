#! /bin/bash

if ! [ -x "$(command -v logrotate)" ]; then
  echo 'Error: logrotate is not installed.' >&2
  sudo apt install logrotate
fi

sudo touch /home/loging-timer.log
sudo touch /home/monitoring.log

sudo cat <<EOF > /etc/logrotate.d/monitoring
/home/logs/app.log {
    maxsize 1M
    rotate 1
    su root root
    create
    copytruncate
}
EOF

# create timer for logrotate
if [ ! -f /etc/systemd/system/logrotate.timer ]; then
  sudo cat <<EOF > /etc/systemd/system/logrotate.timer
[Unit]
Description=Second Log Rotation
Requires=monitoring.service

[Timer]
OnCalendar=*-*-* *:*:0
Unit=monitoring.service
WorkingDirectory=/
StandardOutput=append:/home/loging-timer.log

[Install]
WantedBy=timers.target
EOF
fi

if [ ! -f /etc/systemd/system/monitoring.system ]; then
  sudo cat <<EOF > /etc/systemd/system/monitoring.service
[Unit]
Description=Monitoring Service
Wants=logrotate.timer

[Service]
Type=oneshot
WorkingDirectory=/
ExecStart=/usr/sbin/logrotate /etc/logrotate.d/monitoring
StandardOutput=append:/home/monitoring.log

[Install]
WantedBy=multi-user.target
EOF
fi

if [ ! -d /home/logs/ ]; then
  sudo mkdir /home/logs/
fi
if [ ! -f /home/logs/app.log ]; then
  sudo touch /home/logs/app.log
fi
