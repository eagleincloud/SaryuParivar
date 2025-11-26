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