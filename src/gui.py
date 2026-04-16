#!/usr/bin/env python3

import gi
import math
import random
import threading
import time
import os
import json
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, GLib, Gio, Gdk