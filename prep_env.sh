#!/usr/bin/env bash


## Title: ~/Documents/src/python/pfsense-backup/prep_env.sh
## Description: 
## Author: Joseph Harry <findarato@gmail.com>
## Copyright (C): Joseph Harry 2026
## Date: 2026-04-16 11:09:07
## 
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends --no-install-suggests  ca-certificates && update-ca-certificates 

# Install tools for building
toolDeps="curl xz-utils python3 python3-pip"

apt-get install -y --no-install-recommends --no-install-suggests  $toolDeps

# Install dependencies for Firefox
apt-get install -y --no-install-recommends --no-install-suggests libgl1 libpci3

apt-cache depends firefox-esr | awk '/Depends:/{print$2}'

curl -fL -o /tmp/firefox.tar.xz https://ftp.mozilla.org/pub/firefox/releases/${firefox_ver}/linux-x86_64/en-GB/firefox-${firefox_ver}.tar.xz

tar -xJf /tmp/firefox.tar.xz -C /tmp/
mv /tmp/firefox /opt/firefox
# Download and install geckodriver

curl -fL -o /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_ver}/geckodriver-v${geckodriver_ver}-linux64.tar.gz
tar -xzf /tmp/geckodriver.tar.gz -C /tmp/
chmod +x /tmp/geckodriver
mv /tmp/geckodriver /usr/local/bin/

# Cleanup unnecessary stuff
apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $toolDeps

rm -rf /var/lib/apt/lists/* /tmp/*