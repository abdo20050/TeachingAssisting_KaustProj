$(function(){
    $(".menu i").hide();
    $("#showmenu").click(function(){
      if($(".side-menu").width() > "60"){
        $(".side-menu").animate({width: '-=205px'});
        $(".main-section").animate({'margin-left': '-=205px'});
        $(".logo").text("w");
        $("span.text").hide();
        $(".menu i").show();
        
      }
      else {
          $(".side-menu").animate({width: '+=205px'});
          $(".main-section").animate({'margin-left': '+=205px'});
          $(".logo").text("wiplo");
          $("span.text").show("slow");
          $(".menu i").hide();
      }
      
    });
    
  });


  