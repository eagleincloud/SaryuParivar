// Enhanced Gallery Slider
$('.gallery-slider').owlCarousel({
    loop:true,
    margin:20,
    nav:true,
    dots:true,
    autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause:true,
    navText: ['<i class="bx bx-chevron-left"></i>', '<i class="bx bx-chevron-right"></i>'],
    responsive:{
        0:{
            items:1
        },
        560:{
            items:2
        },
        768:{
            items:3
        },
        991:{
            items: 3
        }
    }
});

// Enhanced Testimonial Slider
$('.testimonial-slider').owlCarousel({
    loop:true,
    margin:20,
    nav:true,
    dots:true,
    autoplay:true,
    autoplayTimeout:4000,
    autoplayHoverPause:true,
    navText: ['<i class="bx bx-chevron-left"></i>', '<i class="bx bx-chevron-right"></i>'],
    responsive:{
        0:{
            items:1
        },
        560:{
            items:1
        },
        768:{
            items:2
        },
        991:{
            items: 3
        }
    }
});

// Scroll Animation Observer
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all fade-in-up elements
document.addEventListener('DOMContentLoaded', function() {
    const fadeElements = document.querySelectorAll('.fade-in-up');
    fadeElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
        observer.observe(el);
    });
    
    // Animate event cards on scroll
    const eventCards = document.querySelectorAll('.event-card');
    eventCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateX(-30px)';
        card.style.transition = `opacity 0.6s ease-out ${index * 0.1}s, transform 0.6s ease-out ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Parallax effect for carousel
    const carousel = document.querySelector('#carouselExampleControls');
    if (carousel) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.5;
            carousel.style.transform = `translateY(${rate}px)`;
        });
    }
});
// const toggleButton = document.getElementById('toggleButton');
// const hiddenDiv = document.getElementById('hiddenDiv');
// toggleButton.addEventListener('click', function() {
//     hiddenDiv.classList.toggle('hidden');
//     hiddenDiv.classList.toggle('opacity-0');
//     if (!hiddenDiv.classList.contains('hidden')) {
//         hiddenDiv.classList.add('opacity-100')
//     }
// });

$("#menu").metisMenu();
$("#btn").click(function(){
    $(".wrapper").toggleClass("active");
    $(".sidebar_wrapper .toggle-icon").removeClass("ms-auto");
    $(".sidebar_wrapper .toggle-icon").addClass("m-auto");
});

// ============================================
// MOBILE DEVICE DETECTION
// ============================================
(function() {
    'use strict';
    
    // Detect mobile device
    function detectMobileDevice() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        
        // Check for mobile devices
        const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent.toLowerCase());
        
        // Check for touch support
        const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        
        // Check screen width
        const isSmallScreen = window.innerWidth <= 768;
        
        // Check for mobile-specific features
        const isMobileDevice = isMobile || (hasTouch && isSmallScreen);
        
        // Check for tablet
        const isTablet = /ipad|android(?!.*mobile)|tablet/i.test(userAgent.toLowerCase()) && window.innerWidth <= 1024;
        
        return {
            isMobile: isMobileDevice,
            isTablet: isTablet,
            hasTouch: hasTouch,
            screenWidth: window.innerWidth
        };
    }
    
    // Apply mobile classes
    function applyMobileClasses() {
        const device = detectMobileDevice();
        const body = document.body;
        
        // Remove existing device classes
        body.classList.remove('mobile-device', 'tablet-device', 'desktop-device');
        
        if (device.isMobile) {
            body.classList.add('mobile-device');
        } else if (device.isTablet) {
            body.classList.add('tablet-device');
        } else {
            body.classList.add('desktop-device');
        }
        
        // Add touch class if touch is supported
        if (device.hasTouch) {
            body.classList.add('touch-device');
        }
        
        // Store device info for later use
        window.deviceInfo = device;
    }
    
    // Run on page load
    document.addEventListener('DOMContentLoaded', function() {
        applyMobileClasses();
        
        // Re-check on resize (with debounce)
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                applyMobileClasses();
            }, 250);
        });
        
        // Re-check on orientation change
        window.addEventListener('orientationchange', function() {
            setTimeout(function() {
                applyMobileClasses();
            }, 100);
        });
    });
    
    // Also run immediately if DOM is already loaded
    if (document.readyState === 'loading') {
        // DOM is still loading
    } else {
        // DOM is already loaded
        applyMobileClasses();
    }
})();

// Mobile sidebar overlay handler
document.addEventListener('DOMContentLoaded', function() {
    // Create sidebar overlay for mobile
    if (!document.querySelector('.sidebar-overlay')) {
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.addEventListener('click', function() {
            document.querySelector('.wrapper').classList.remove('active');
        });
        document.body.appendChild(overlay);
    }
    
    // Close sidebar when clicking outside on mobile
    const sidebarToggle = document.getElementById('btn');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            const wrapper = document.querySelector('.wrapper');
            if (window.deviceInfo && window.deviceInfo.isMobile) {
                // On mobile, toggle overlay
                const overlay = document.querySelector('.sidebar-overlay');
                if (wrapper.classList.contains('active')) {
                    overlay.style.display = 'block';
                } else {
                    overlay.style.display = 'none';
                }
            }
        });
    }
});