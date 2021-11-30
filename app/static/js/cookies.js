var codeContent = 'Choose a language to start.';
jQuery('#codeBlock').html('');
var problem_id = jQuery('#problem').text();
var judgeLangId =  71;
var responseLang = 'python';
current_user_id = jQuery('#user_id').text();
var contest_id = jQuery('#contest_id').text();

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

if(getCookie(problem_id+current_user_id)){
  var cookie = getCookie(problem_id+current_user_id);
  var key = "2e35f242a46d67eeb74aabc37d5e5d05";
  var code = CryptoJS.AES.decrypt(cookie, key).toString(CryptoJS.enc.Utf8);;
  var monacoId = getCookie('monacoId'+problem_id+current_user_id);
  var judgeId = getCookie('judgeId'+problem_id+current_user_id);
}

if(code) {
    codeContent = code;
}
if(monacoId) {
  responseLang = monacoId;  
}
if (judgeId) {
  judgeLangId = judgeId;
}

jQuery('#languages').on('change', function() {
  judgeLangId = jQuery(this).children(":selected").attr("id");
  responseLang = jQuery(this).val();
  document.cookie = "judgeId"+problem_id+current_user_id+"="+ judgeLangId; +"; expires=Fri, 18 Dec 2021 12:00:00 UTC; path=/"; 
  document.cookie = "monacoId"+problem_id+current_user_id+"="+ responseLang; +"; expires=Fri, 18 Dec 2021 12:00:00 UTC; path=/";
});