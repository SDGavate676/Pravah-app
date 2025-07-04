// (function ($) {
//     "use strict";

//     // Sticky Navbar
//     $(window).scroll(function () {
//         if ($(this).scrollTop() > 40) {
//             $('.navbar').addClass('sticky-top');
//         } else {
//             $('.navbar').removeClass('sticky-top');
//         }
//     });
    
//     // Dropdown on mouse hover
//     $(document).ready(function () {
//         function toggleNavbarMethod() {
//             if ($(window).width() > 992) {
//                 $('.navbar .dropdown').on('mouseover', function () {
//                     $('.dropdown-toggle', this).trigger('click');
//                 }).on('mouseout', function () {
//                     $('.dropdown-toggle', this).trigger('click').blur();
//                 });
//             } else {
//                 $('.navbar .dropdown').off('mouseover').off('mouseout');
//             }
//         }
//         toggleNavbarMethod();
//         $(window).resize(toggleNavbarMethod);
//     });

//     function handleLogin(event) {
//         // Prevent default anchor behavior (no navigation yet)
//         event.preventDefault();
    
//         // Ask for confirmation before proceeding
//         if (confirm("Are you sure you want to log in?")) {
//           // Redirect to the login page using Django's rendered URL
//           window.location.href = "{% url 'login' %}";
//         }
//       }

  
    
//     // Back to top button
//     $(window).scroll(function () {
//         if ($(this).scrollTop() > 100) {
//             $('.back-to-top').fadeIn('slow');
//         } else {
//             $('.back-to-top').fadeOut('slow');
//         }
//     });
//     $('.back-to-top').click(function () {
//         $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
//         return false;
//     });






//     // Testimonials carousel
//     $(".testimonial-carousel").owlCarousel({
//         autoplay: true,
//         smartSpeed: 1000,
//         items: 1,
//         dots: false,
//         loop: true,
//         nav : true,
//         navText : [
//             '<i class="bi bi-arrow-left"></i>',
//             '<i class="bi bi-arrow-right"></i>'
//         ],
//     });
    
// })(jQuery);


// scripts.js (external JS file)

(function ($) {
    "use strict";

    // Handle login action
    function handleLogin(event) {
        // Prevent default anchor behavior (no navigation yet)
        event.preventDefault();

        // Get the login URL from the data attribute
        var loginUrl = $('#loginButton').data('login-url');

        // Ask for confirmation before proceeding
        if (confirm("Are you sure you want to log in?")) {
            // Redirect to the login page using the URL stored in the data attribute
            window.location.href = loginUrl;
        }
    }

    // Attach the handleLogin function to the click event of the login button
    $('#loginButton').on('click', handleLogin);

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 40) {
            $('.navbar').addClass('sticky-top');
        } else {
            $('.navbar').removeClass('sticky-top');
        }
    });
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
    });
})(jQuery);
