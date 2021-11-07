var globalVariable={
    editorCodeBlock: monaco.editor
};
    globalVariable.editorCodeBlock = monaco.editor.create(document.getElementById("codeBlock"), {
    value: codeContent,
    language: responseLang,
    theme: "vs-dark",
    lineNumbers: 'on',
    glyphMargin: false,
    vertical: 'auto',
    horizontal: 'auto',
    verticalScrollbarSize: 10,
    horizontalScrollbarSize: 10,
    scrollBeyondLastLine: false,
    readOnly: false,
    automaticLayout: true,
    minimap: {
        enabled: false
    },
    lineHeight: 19,
    contextmenu: false
});
jQuery('#codeBlock').height('100%');
jQuery('#codeBlock').width('100%');
    
jQuery('#languages').on('change', function() {
    responseLang = jQuery(this).val();
    jQuery('.codeBlock').html('');
    globalVariable.editorCodeBlock = monaco.editor.create(document.getElementById("codeBlock"), {
        value: '',
        language: responseLang,
        fontFamily: 'monospace',
        theme: "vs-dark",
        lineNumbers: 'on',
        glyphMargin: false,
        vertical: 'auto',
        horizontal: 'auto',
        verticalScrollbarSize: 10,
        horizontalScrollbarSize: 10,
        scrollBeyondLastLine: false,
        readOnly: false,
        automaticLayout: true,
        minimap: {
            enabled: false
        },
        lineHeight: 19,
        contextmenu: false
    });
    document.fonts.ready.then(() => {
        editorCodeBlock.editor.remeasureFonts()
    })
    jQuery('#codeBlock').height('100%');
    jQuery('#codeBlock').width('100%');
});

setInterval(function(){
    var key = "2e35f242a46d67eeb74aabc37d5e5d05";
    var value = CryptoJS.AES.encrypt(globalVariable.editorCodeBlock.getValue(), key);
    document.cookie = problem_id+current_user_id+"="+value+"; expires=Fri, 18 Dec 2021 12:00:00 UTC; path=/";
  }, 3000);

document.getElementById(judgeId).selected = true;

function goFullScreen(){
    var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
        (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
        (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
        (document.msFullscreenElement && document.msFullscreenElement !== null);

    var elem = document.getElementById('block');
    if (!isInFullScreen) {
        if(elem.requestFullscreen){
            elem.requestFullscreen();
        }
        else if(elem.mozRequestFullScreen){
            elem.mozRequestFullScreen();
        }
        else if(elem.webkitRequestFullscreen){
            elem.webkitRequestFullscreen();
        }
        else if(elem.msRequestFullscreen){
            elem.msRequestFullscreen();
        }
    }
    else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } 
        else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } 
        else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } 
        else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}