#!/bin/bash

# Check BBR support in kernel

A=`grep 'CONFIG_TCP_CONG_BBR' /boot/config-$(uname -r)`
RA=$?
B=`grep 'CONFIG_NET_SCH_FQ' /boot/config-$(uname -r)`
RB=$?
C=`egrep 'CONFIG_TCP_CONG_BBR|CONFIG_NET_SCH_FQ' /boot/config-$(uname -r)`
RC=$?

echo $A
echo $B
echo $C

if [[ $RA != 0 || $RB != 0 || $RC != 0 ]] ; then
	echo "Warning! Your kernel has not BBR support!" 1>&2
else
	echo "Cogratulations! Your kernel supports BBR."
fi;


DEBIAN_FRONTEND=noninteractive

# Easy way -> tc issue due to tq missing option in mininet if BBR is used
# apt-get -y install mininet


# Install compiling from source, may take a while
git clone git://github.com/mininet/mininet
cd  mininet
git checkout 2.3.0d4 -b 2.3.0d4

# Apply fq patch - https://sdn-lab.com/2017/10/10/tcp-bbr-congestion-control-on-mininet/
wget https://github.com/castroflavio/mininet/commit/9614a9445249b898cb4ed2d56c3699ca19c38e01.patch -O fq.patch
git apply fq.patch

# Compile and install
./util/install.sh -a


# TO CONNECT:
#ssh vagrant@127.0.0.1 -p 2222 -i .vagrant/machines/mininet-1/virtualbox/private_key -X
#sed -i "s/#X11UseLocalhost yes/X11UseLocalhost no/" /etc/ssh/sshd_config
echo 'X11UseLocalhost no' >> /etc/ssh/sshd_config

apt-get install -y tmux nginx

# Disable dameon
echo "daemon off;" >> /etc/nginx/nginx.conf
service nginx stop
rm /var/www/html/index.nginx-debian.html
cp /home/vagrant/DNCS_BBR/http_test/page /var/www/html/web_page/
