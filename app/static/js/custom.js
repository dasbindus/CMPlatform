/*=============================================================
      Authour URI: www.binarytheme.com
      License: Commons Attribution 3.0
  
      http://creativecommons.org/licenses/by/3.0/
  
      100% To use For Personal And Commercial Use.
      IN EXCHANGE JUST GIVE US CREDITS AND TELL YOUR FRIENDS ABOUT US
     
      ========================================================  */



jQuery(function ($) {

    /*==========================================
 CUSTOM SCRIPTS 
  =====================================================*/
    //  LOADING SCRIPTS FUNCTION
    $(window).load(function () {
        $(".loader").fadeOut("slow");
    });
      
    // PRETTYPHOTO FUNCTION 

    $("a.preview").prettyPhoto({
        social_tools: false
    });

    //ISOTOPE FUNCTION - FILTER PORTFOLIO FUNCTION
    $(window).load(function () {
        $portfolio = $('.portfolio-items');
        $portfolio.isotope({
            itemSelector: 'li',
            layoutMode: 'fitRows'
        });
        $portfolio_selectors = $('.portfolio-filter >li>a');
        $portfolio_selectors.on('click', function () {
            $portfolio_selectors.removeClass('active');
            $(this).addClass('active');
            var selector = $(this).attr('data-filter');
            $portfolio.isotope({ filter: selector });
            return false;
        });
    });


    /*==========================================
    WRITE  YOUR  SCRIPTS BELOW
    =====================================================*/

});