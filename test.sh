#!/usr/bin/env bash


## Title: ~/Documents/src/python/pfsense-backup/test.sh
## Description: 
## Author: Joseph Harry <findarato@gmail.com>
## Copyright (C): Joseph Harry 2026
## Date: 2026-04-16 10:47:25
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


podman build --tag pfsense . 
# podman run --rm -v $(pwd):/app pfsense pytest -v
podman run --rm localhost/pfsense:latest