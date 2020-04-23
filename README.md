# BurpApkRepacking
### A python script bypassing default CA restrictions in Android

### The APK after repacking is possible to use with Burp Suite on device with Android 7 and above [without ROOT] 

## Platforms
* Mac
* Linux / Unix

## Requirements

Python 3 & apktool, keytool, jarsigner

### Installation

**Apktool** 

https://ibotpeaches.github.io/Apktool/install/

**keytool, jarsigner** 

apt install openjdk-11-jdk-headless

## Usage

```
python3 burp_apk_repacking.py name.apk
```
## Result
```
YOUR APK ==> NEW_name.apk
```
## Processes
1. Disassembling the APK (Apktool)
2. Updating network_security_config.xml
3. Updating AndroidManifest.xml
4. Building new the APK (Apktool)
5. Creating new keystore (keytool)
6. Self-signing the APK (jarsigner)
7. Deleting temp files

###### Tested with Apktool 2.4.1, Android 9
