$(document).ready(function(){
    var $regexname=/^([a-zA-Z]{3,16})$/;
    var $regexemail=/([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?/;
    var $regexpass=/(?=.{6,})/;
    $('.pwd').on('keypress keydown keyup',function(){
      if(!$(this).val().match($regexepass)){
        $('.emsg').removeClass('hidden');
        $('.emsg').show();
      }
      else{
        $('.emsg').addClass('hidden');
      }
    })
    $('.email').on('keypress keydown keyup',function(){
      if(!$(this).val().match($regexemail)){
        $('.emsg').removeClass('hidden');
        $('.emsg').show();
      }
      else{
        $('.emsg').addClass('hidden');
      }
    })
    $('.name').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexname)) {
              // there is a mismatch, hence show the error message
                 $('.emsg').removeClass('hidden');
                 $('.emsg').show();
             }
           else{
                // else, do not display message
                $('.emsg').addClass('hidden');
               }
         });
});