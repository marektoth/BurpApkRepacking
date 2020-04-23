#!bin/python3

#
# Requirements: apktool, keytool, jarsigner
# Syntax: python3 burp_apk_repacking.py name.apk
#
# BurpApkRepacking (v0.1)
# Date: 2020-04-23
# Created by: Marek Toth
#

import sys, os, xml.etree.ElementTree as ET 

if not sys.version.startswith('3'):
	print('\nThis script works only with Python3\n')
	sys.exit()

def printTitle(process):
	print("-" * 50)
	print(f"{process}")
	print("-" * 50)

def updateXML(folderName):
	printTitle("Updating/Creating XML file")
	path = f"{folderName}/res/xml/network_security_config.xml"
	network_security_config = ET.Element('network-security-config')
	base_config = ET.SubElement(network_security_config, 'base-config')
	trust_anchors = ET.SubElement(base_config, 'trust-anchors')
	ET.SubElement(trust_anchors, 'certificates', src='user')
	ET.SubElement(trust_anchors, 'certificates', src='system')
	ET.ElementTree(network_security_config).write(path)
	print("I: network_security_config.xml updated\n")

def editAndroidManifest(folderName):
	printTitle("Updating AndroidManifest")
	path = f"{folderName}/AndroidManifest.xml"
	tree = ET.parse(path)
	root = tree.getroot()
	for config in root.iter('application'):
		config.set('{http://schemas.android.com/apk/res/android}networkSecurityConfig', '@xml/network_security_config')
	ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
	ET.ElementTree(root).write(path, xml_declaration=True, encoding="utf-8")
	print("I: AndroidManifest.xml updated\n")

def disassemblingAPK(apk):
	printTitle("Disassembling the APK")
	disasembling = f"apktool d {apk}"
	os.system(disasembling)

def buildingAPK(folderName):
	printTitle("Building new the APK")
	repackaging = f"apktool b {folderName}"
	os.system(repackaging)

def creatingKeystore():
	printTitle("Creating new keystore")
	key = "keytool -genkey -v -noprompt -keystore test.keystore -storepass password -alias android -dname 'CN=TEST, OU=TEST, O=TEST, L=TEST, S=TEST, C=TEST' -keypass password -keyalg RSA -keysize 2048 -validity 10000  > /dev/null"
	os.system(key)

def signingAPK(name):
	printTitle("Self-signing the APK")
	sign = f"jarsigner -verbose -keystore test.keystore -storepass password -keypass password {name}/dist/{name}.apk android  > /dev/null"
	os.system(sign)
	print("I: APK self-signed")

def main():
	apk = sys.argv[1]
	if (len(sys.argv) == 2)&(apk.lower().endswith(".apk")):
		if os.path.exists(apk):		
			name = apk[:-4]
			if (apk.endswith(".APK")):
				folderName = f"{name}.APK.out"
			else:
				folderName = name
		else:
			print(f"File {apk} not found!")
			sys.exit()
	else:
		print("Error: Invalid amout of arguments\n")
		print("Syntax: python3 burp_apk_repacking.py name.apk\n")
		sys.exit()

	print("""
########################################################################
#                                                                      #
#                       BurpApkRepacking (v0.1)                        #
#  A script to repackage an APK to allow a user-installed certificate  #
#                                                                      #
########################################################################
""")

	# Disassembling the APK
	disassemblingAPK(apk)

	# Updating XML file
	updateXML(folderName)

	# Updating AndroidManifest
	editAndroidManifest(folderName)

	# Building new the APK
	buildingAPK(folderName)

	# Creating new keystore
	creatingKeystore()

	# Self-signing the APK
	signingAPK(name)

	# Deleting temp files
	if os.path.exists(f"{folderName}/dist/{apk}"):
		os.system(f"cp {folderName}/dist/{apk} NEW_{name}.apk")
		os.system("rm test.keystore")		
		os.system(f"rm -r {folderName}")
		print(f"""
#####################################################
#                                                   #
#              COMPLETED - APK PATCHED              #
#                                                   #
#####################################################

YOUR APK ==> NEW_{name}.apk
	""")

	else:
		print(f"File {folderName}/dist/{apk} not found!")
		sys.exit() 

if __name__ == '__main__':
	main()