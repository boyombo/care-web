$(function ($) {
    "use strict";

    //veno-box js
    $('.venobox').venobox();

    var $window = $(window);
    var html_body = $('html, body')


    //for scroll bottom to top js here
    if ($('.totop').length) {
        var scrollTrigger = 150, // px
            backToTop = function () {
                var scrollTop = $(window).scrollTop();
                if (scrollTop > scrollTrigger) {
                    $('.totop').addClass('show');
                } else {
                    $('.totop').removeClass('show');
                }
            };

        backToTop();
        $window.on('scroll', function () {
            backToTop();
            if ($window.scrollTop()) {
                $("#mainHeader").addClass('stiky');
            } else {
                $("#mainHeader").removeClass('stiky');
            }
        });

        $('.totop').on('click', function (e) {
            e.preventDefault();
            $('html,body').animate({
                scrollTop: 0
            }, 700);
        });
    }

    // counter js
    $('.count').counterUp({
        delay: 10,
        time: 2000
    });

  // banner slider
  var $mainSlider = $('.silder');

  $mainSlider.owlCarousel({
  loop: true,
  navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
  nav: true,
  dots:false,
  autoplay: true,
  autoplayTimeout: 3000,
  animateOut: 'fadeOut',
  animateIn: 'fadeIn',
  smartSpeed: 450,
  responsive: {
      0: {
          items: 1,
          nav:false
      },
      768: {
          items: 1,
          nav:false,
      },
      960: {
          items: 1,
          nav:false
      },
      1250: {
          items: 1
      },
      1920: {
          items: 1
      }
  }
});

    // testimonialSlider
    $('.testimonialSlider').owlCarousel({
        loop: true,
        margin: 30,
        nav: true,
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
            },
            576: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    })

    //Site Preloader
    jQuery(window).on('load', function () {
        var $sitePreloaderSelector = $('.site-preloader');
        $sitePreloaderSelector.fadeOut(500);


    });


}(jQuery));