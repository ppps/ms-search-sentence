function getEditor() {
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
