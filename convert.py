import os
import sys
try:
	import lz4.frame
except:
	print('Do "pip install lz4" in order to use this')
	sys.exit(-1)

if __name__ == "__main__":
	path = "C:\\Users\\<username>\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\<profile>\\sessionstore-backups\\recovery.jsonlz4"

	json = None
	with lz4.frame.open(path, mode='rb') as f:
		data = f.read()

	with open("out.json", 'w') as f:
		f.write(json)

# https://www.reddit.com/r/firefox/comments/2ps6wg/jsonlz4_bookmark_backups/
# 1. about:config -> enable "devtools.chrome.enabled"
# 2. Open Scratchpad (shift+F4)
# 3. Set Enviroment to "Browser"
# 4. Run the following (setting the path before hand)
"""
var file="C:\\Users\\<username>\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\<profile>\\sessionstore-backups\\recovery.jsonlz4";
OS.File.read(file, { compression: "lz4" }).then(bytes => {
  OS.File.writeAtomic(file + ".uncompressed", JSON.stringify(JSON.parse(new TextDecoder().decode(bytes)),null,2))
});
"""

# lz4 decompress: https://github.com/steeve/python-lz4
# sessionstore is lz4 compressed JSON in sessionstore-backups (use latest one by time)
# simplified tab group
# - SessionStorage: https://github.com/denschub/firefox-tabgroups/blob/develop/src/lib/storage/session.js
# - TabManager: https://github.com/denschub/firefox-tabgroups/blob/develop/src/lib/tabmanager.js
# Sync tab groups: Can probably just look at a backup file from laptop and reproduce format
