[app]
title = Mi Alarma
package.name = mialarma
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3,ogg

version = 1.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

android.permissions = WAKE_LOCK,VIBRATE
android.allow_background = True
android.api = 33
android.minapi = 21
