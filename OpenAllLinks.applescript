tell application "Safari"
	tell the front document
		set articleURLs to do JavaScript "Array.from(document.querySelectorAll('.edit a')).map((el) => el.href)"
	end tell
	tell window 1
		repeat with aURL in articleURLs
			set current tab to (make new tab with properties {URL:aURL})
		end repeat
	end tell
end tell