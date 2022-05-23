var quizDelayShowAnswers = 3000
var quizDelayFreezeButton = 10000


$(document).on('click', '.quizanswer',  function(){$(this).toggleClass("toggle");});

var quizshowanswers = function(quizid, quizbutton){

    str = "#"+quizid.id+" .row .quizanswer"; 


    // We do not accept no answers picked:

    var notpressed = true;
    
    $(str).each(
	function(){
	    obj = $(this);
	    if (obj.hasClass("toggle"))
		notpressed = false;
	}
    );

    if (notpressed)
	return;
    
    $(str).each(
    function(){
    obj = $(this);
    if (obj.attr("datav") == "F")
      obj.addClass("quizwronganswer");
    else
      obj.addClass("quizrightanswer");
    });
    setTimeout(function(){
    $(str).each(
    function(){
      obj=$(this);
      if (obj.attr("datav") == "F")
        obj.removeClass("quizwronganswer");
      else
        obj.removeClass("quizrightanswer");
      obj.removeClass("toggle");
      obj.addClass("quizanswer");
      })}, quizDelayShowAnswers);

    strbutton="#" + quizbutton.id;

    $(strbutton).attr("disabled", true);
    setTimeout(function(){
	$(strbutton).attr("disabled", false);
    }, quizDelayFreezeButton);
};

 
