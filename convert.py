import json

def parseGroupData(sessionstore):
	import io

	session = {}
	with io.open(sessionstore, mode='r', encoding="utf-8") as f:
		session = json.load(f)

	groups = []
	for window in session["windows"]:
		windowGroup = {}

		if window["extData"] and window["extData"]["tabview-group"]:
			groupParsed = json.loads(window["extData"]["tabview-group"])
			groupsParsed = json.loads(window["extData"]["tabview-groups"])

			activeGroupId = groupsParsed["activeGroupId"]

			for groupId in groupParsed:
				group = groupParsed[groupId]
				windowGroup[group["id"]] = {
					"title": group["title"],
					"tabs": []
				}

			for tab in window["tabs"]:
				if len(tab["entries"]) > 0 and tab["extData"] and tab["extData"]["tabview-tab"]:
					tabGroupUi = json.loads(tab["extData"]["tabview-tab"])

					entry0 = tab["entries"][0]

					windowGroup[tabGroupUi["groupID"]]["tabs"].append({
						"title": entry0["title"],
						"url": entry0["url"], #if entry0["originalURI"]: entry0["originalURI"] else: entry0["url"],
						"icon": tab["image"],
						"hidden": tab["hidden"],
						"lastAccessed": tab["lastAccessed"],
					})
		groups.append(windowGroup)

	return groups

def convert(sessionstore):
	groups = parseGroupData(sessionstore)

	sync_tab_data = {
		"version": [
			"syncTabGroups",
			1
		],
		"groups": []
	}

	tabIndex = 0
	groupCounter = 0
	windowGroupCounter = 0
	for group in groups:
		for groupIndex in group:
			tabGroup = {
				"title": "Window {0} - {1}".format(windowGroupCounter + 1, group[groupIndex]["title"]),
				"tabs": [],
				"id": groupCounter + 1,
				"windowId": -1, #??
				"index": groupCounter,
				"position": groupCounter,
				"expand": False,
				"lastAccessed": 0,
				"incognito": False
			}
			groupCounter = groupCounter + 1

			for tab in group[groupIndex]["tabs"]:
				tabGroup["tabs"].append({
					"title": tab["title"],
					"url": tab["url"],
					"favIconUrl": tab["icon"],
					"hidden": False, #tab["hidden"]
					"lastAccessed": tab["lastAccessed"],
					"pinned": False,
					"windowId": tabGroup["windowId"],
					"discarded": False,
					"active": False,
					"id": tabIndex
				})
				tabIndex = tabIndex + 1

			sync_tab_data["groups"].append(tabGroup)
		windowGroupCounter = windowGroupCounter +1

	print(json.dumps(sync_tab_data, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Convert from 'Simplified Tab Groups' (by Dennis Schubert) tab group data to 'Sync tab groups' (by Morikko) tab group data")
	parser.add_argument('-a', '--about', action="store_true", help="What this program is supposed to do. Note: add some random value to get the program to not complain about sessionstore being required...")
	parser.add_argument('sessionstore')

	args = parser.parse_args()

	if args.about:
		print("\nFirefox used to have a feature called 'Tab Groups' for powerusers to group tabs together\n")
		print("Firefox got rid of this feature due to lack of use... fast foward, they are adding in API support (tab hidding) for this because there has been such a demand for it. So much for lack of use.\n")
		print("In the mean time, users of the feature have hopped extension to extension for whatever provided an equivilent experience and feature. Many users, such as myself, switched to 'Simplified Tab Groups' (by Dennis Schubert)\n")
		print("But Mozilla was continuing their move to 'be like Chrome instead of like Firefox' and that move included switching to WebExtensions which didin't allow for tab hiding (and as one FF dev put it: 'I'm not so sure about adding tab hiding to WebExtensions. Chrome doesn't have it...), and Dennis said it took Mozilla so long to switch, that he moved away from using tab groups and now doesn't have a reason to update the extension to support the feature.\n")
		print("Mozilla has since added beta functionality for the tab hiding and extensions have since added support for it. But there's a catch: WebExtensions appeared in FF 57, but the new API doesn't exist until FF 59... and so all the extensions that support the feature require FF 59 and higher to work. How do you switch from FF 56 or earlier to 59 without loosing your tab groups?\n")
		print("Enter 'Sync tab groups' (by Morikko) and this utility. Sync tab groups is a 'mock' tab group extension (switching tabs doesn't hide the tabs, it closes the tabs and opens new ones) and while they're adding support for tab hiding, I've found a different use: they work on FF 56 AND FF 59. Meaning I can switch from FF 56 to a modern FF using the extension, and possibly evaluate other extensions in the mean time.\n")
		print("'And this utility?' you ask, Sync tab groups supports Simplified Tab Groups's and other tab formats to allow easy switching, but it requires the sessionstore data to read extensions from and... enter Mozilla, they changed the format a few versions prior to FF 56 so it's not compressed, in a different location, etc. and Sync tab groups doesn't support that format.\n")
		print("This utility is to convert from the compressed sessionstore to a Sync tab groups format that can simply be imported. I opted to skip the uncompress and use the built in loaded, to reduce chances of failure to load.\nOne catch right now: the utility can't decompress the files itself because FF uses a non-standard version of LZ4 compression\n")
		print("To get your data, do the following: wait a few minutes so that FF will save a recovery sessionstore. It doesn't this periodically (I think about every 10 min), then...")
		print("1. about:config -> enable 'devtools.chrome.enabled'")
		print("2. Open Scratchpad (shift+F4)")
		print("3. Set Enviroment to 'Browser'")
		print("4. Run the following (setting the path before hand)")
		print("================")
		print('var file="C:\\Users\\<user>\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\<profile>\\sessionstore-backups\\recovery.jsonlz4";')
		print('OS.File.read(file, { compression: "lz4" }).then(bytes => {')
		print('  OS.File.writeAtomic(file + ".uncompressed", JSON.stringify(JSON.parse(new TextDecoder().decode(bytes)),null,2))')
		print('});')
		print("================\n")
		print("This will save a file 'recovery.jsonlz4.uncompressed' in the same folder as the recovery file, but now this utility can read it\n")
		print("If that doesn't work, try https://gist.github.com/jscher2000/07f94249b0a5f6d565fb20d88b73bb91 (instructions at top) which came from a mod on Mozilla's forums: https://support.mozilla.org/en-US/questions/1179363#answer-1018017\n")
		print("You're now ready to switch to a new version of Firefox... good luck")
	else:
		convert(args.sessionstore)

'''
import os
import sys
try:
	import lz4.frame
except:
	print('Do "pip install lz4" in order to use this')
	sys.exit(-1)

if __name__ == "__main__":
	path = "C:\\Users\\<user>\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\<profile>\\sessionstore-backups\\recovery.jsonlz4"

	json = None
	with lz4.frame.open(path, mode='rb') as f:
		data = f.read()

	with open("out.json", 'w') as f:
		f.write(json)
'''