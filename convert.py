# https://www.reddit.com/r/firefox/comments/2ps6wg/jsonlz4_bookmark_backups/
# 1. about:config -> enable "devtools.chrome.enabled"
# 2. Open Scratchpad (shift+F4)
# 3. Set Enviroment to "Browser"
# 4. Run the following (setting the path before hand)
"""
var file="C:\\Users\\<user>\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\<profile>\\sessionstore-backups\\recovery.jsonlz4";
OS.File.read(file, { compression: "lz4" }).then(bytes => {
  OS.File.writeAtomic(file + ".uncompressed", JSON.stringify(JSON.parse(new TextDecoder().decode(bytes)),null,2))
});
"""

import argparse

if __name__ == "__main__":
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
		print("You're now ready to switch to a new version of Firefox... good luck")
	else:
		sessionstore = args.sessionstore

		sync_tab_data = {
			"version": [
				"syncTabGroups",
				1
			],
			"groups": []
		}

		# <per-window> (sessionstore -> windows -> <index>)
		# <getting groups>
		#extData -> tabview-group -> <parseJson> -> <group ID> -> "title" (also, assign a unique group ID but keep a map between the two and add the window index to the window)
		# <getting active groups>
		#extData -> tabview-groups -> <parseJson> -> "activeGroupId"
		# <getting tabs for a group>
		#tabs -> <index> -> extData -> tabview-tab -> <parseJson> -> "groupId" (map to the unique group ID)

		# Creating the new list:
		# Populate "groups" with each group. Title and unique ID appended to the list. (windowId = -1, position = <the order the list should be shown in UI>, expand/incognito = false, lastAccess = 0)
		# each tab ??

		#TODO

		print(sync_tab_data)
		