# BurpApkRepacking
**A python script bypassing default CA restrictions in Android.** 

After the process is possible to **work with Burp Suite on devices with Android 7 and above.**

## Platforms
* Mac
* Linux / Unix

## Requirements

Python 3 & apktool, keytool, jarsigner

### Installation

**Apktool**

- https://ibotpeaches.github.io/Apktool/install/

**keytool, jarsigner**
```
apt install openjdk-11-jdk-headless
```
## Usage

```
python3 burp_apk_repacking.py name.apk
```