on theSplit(theString, theDelimiter)
	-- save delimiters to restore old settings
	set oldDelimiters to AppleScript's text item delimiters
	-- set delimiters to delimiter to be used
	set AppleScript's text item delimiters to theDelimiter
	-- create the array
	set theArray to every text item of theString
	-- restore the old setting
	set AppleScript's text item delimiters to oldDelimiters
	-- return the result
	return theArray
end theSplit

tell application "Safari"
	tell the front document
		do JavaScript "function getEditor() {
    return CKEDITOR.instances['edit-body-und-0-value'];
}

function getHTML() {
    return getEditor().getData();
}

function setHTML(html) {
    return getEditor().setData(html);
}

function firstParagraph(html) {
    return html.split('</p>', 1)[0].slice(3);
}

function setTitle(text) {
    return document.querySelector('#edit-title').value = text;
}

function setStandfirst(text) {
    return document.querySelector('#edit-field-lead-und-0-value').value = text;
}

function codePointsJSON(text) {
    return JSON.stringify(
        Array.from(text).map(c => c.codePointAt(0))
    );
}

function setReadyForPublishing() {
    // 4 is the index of the `Ready for Publishing` state
    var el = document.querySelector('#edit-workbench-moderation-state-new');
    return el.selectedIndex = 4;
}

function saveAndClose() {
    document.querySelector('#edit-submit-1').click();
}
"
		set firstParCodePoints to do JavaScript "codePointsJSON(firstParagraph(getHTML()))"
		set fromNetwork to (do shell script "curl http://192.168.1.20:5000/lookup -X POST -F codeunits=" & firstParCodePoints)
		
		set articleDetails to my theSplit(fromNetwork, "|")
		set title to the first item of articleDetails
		set standfirst to the second item of articleDetails
		
		if title is not "Title not found" then
			do JavaScript "setTitle(" & quote & title & quote & ")"
			do JavaScript "setStandfirst(" & quote & standfirst & quote & ")"
			do JavaScript "setReadyForPublishing()"
			
			if button returned of (display dialog "Save and close?") is "OK" then
				do JavaScript "saveAndClose()"
			end if
		else
			display dialog "Could not find a title in the database"
		end if
		
	end tell
end tell
