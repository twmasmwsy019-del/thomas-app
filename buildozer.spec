[app]
title = Thomas Supermarket
package.name = thomasapp
package.domain = org.thomas
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 0.1
requirements = python3,kivy,pillow,qrcode,arabic_reshaper,python-bidi

orientation = portrait
osx.kivy_version = 2.0.0
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

[buildozer]
android.accept_sdk_license = True
log_level = 2
warn_on_root = 1

