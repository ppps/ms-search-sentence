tell application "Safari"
	tell the front document
		set firstPar to do JavaScript "JSON.stringify(Array.from(CKEDITOR.instances['edit-body-und-0-value'].getData().split('</p>', 1)[0].slice(3)).map(c => c.codePointAt(0)))"
	end tell
end tell

-- do shell script "LANG=en_GB.UTF-8 LC_CTYPE=en_GB.UTF-8 LC_ALL=en_GB.UTF-8 echo " & firstPar & " | /usr/local/bin/python3 /Users/admin/projects/sentence-search/db_search.py -j "

set foundTitle to do shell script "(export LC_ALL=en_GB.UTF-8 && echo " & firstPar & " | /usr/local/bin/python3 /Users/admin/projects/sentence-search/db_search.py -j)"

