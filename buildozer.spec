[app]

title = Thomas Supermarket
package.name = thomasapp
package.domain = org.thomas
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 0.1
requirements = python3,kivy,pillow,qrcode
orientation = portrait

# تحديد إصدارات مستقرة لتجنب مشاكل البناء
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1
android.accept_sdk_license = True
