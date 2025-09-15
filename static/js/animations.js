// Animation on Scroll
document.addEventListener('DOMContentLoaded', function() {
    // Animate elements when they come into view
    const animatedElements = document.querySelectorAll('.feature-card, .step, .testimonial, .scholarship-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeIn');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Floating card animations
    const floatingCards = document.querySelectorAll('.floating-card');
    floatingCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.5}s`;
    });
    
    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.classList.add('btn-animate');
    });
    
    // Hero text animation
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        heroTitle.classList.add('animate-slideInLeft');
    }
    
    const heroDescription = document.querySelector('.hero-description');
    if (heroDescription) {
        heroDescription.classList.add('animate-slideInRight');
        heroDescription.style.animationDelay = '0.3s';
    }
    
    const heroButtons = document.querySelector('.hero-buttons');
    if (heroButtons) {
        heroButtons.classList.add('animate-fadeIn');
        heroButtons.style.animationDelay = '0.6s';
    }
    
    // Background particle animation
    animateParticles();
    
    // Text shimmer effect for headings
    const headings = document.querySelectorAll('.section-title, .hero-title');
    headings.forEach(heading => {
        const words = heading.textContent.split(' ');
        heading.innerHTML = words.map(word => {
            if (word.includes('span')) return word;
            return `<span class="text-shimmer">${word}</span>`;
        }).join(' ');
    });
});

// Particle animation
function animateParticles() {
    const particles = document.querySelectorAll('.particle');
    particles.forEach(particle => {
        const randomX = (Math.random() - 0.5) * 100;
        const randomY = (Math.random() - 0.5) * 100;
        particle.style.setProperty('--move-x', `${randomX}vw`);
        particle.style.setProperty('--move-y', `${randomY}vh`);
        
        // Randomize animation duration
        const duration = 15 + Math.random() * 15;
        particle.style.animationDuration = `${duration}s`;
    });
}

// Typewriter effect
function typeWriter(element, speed = 100) {
    if (!element) return;
    
    const text = element.textContent;
    element.textContent = '';
    element.style.borderRight = '0.15em solid #4e54c8';
    
    let i = 0;
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        } else {
            element.style.borderRight = 'none';
        }
    }
    type();
}

// Initialize typewriter effect on elements with class 'typewriter'
document.addEventListener('DOMContentLoaded', function() {
    const typewriterElements = document.querySelectorAll('.typewriter');
    typewriterElements.forEach(element => {
        typeWriter(element);
    });
});

// Progress bar animation
function animateProgressBar() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        bar.style.animation = 'progress 3s ease-in-out';
    });
}

// Card flip animation
function initCardFlip() {
    const flipCards = document.querySelectorAll('.flip-card');
    flipCards.forEach(card => {
        card.addEventListener('click', function() {
            this.querySelector('.flip-card-inner').classList.toggle('flipped');
        });
    });
}

// Parallax effect
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = parseFloat(element.getAttribute('data-speed')) || 0.5;
            element.style.transform = `translateY(${scrollTop * speed}px)`;
        });
    });
}

// Initialize animations when page loads
window.addEventListener('load', function() {
    initCardFlip();
    initParallax();
    animateProgressBar();
});

// Count-up animation
function animateValue(element, start, end, duration) {
    if (!element) return;
    
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value.toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Initialize counter animations when in viewport
function initCounters() {
    const counterElements = document.querySelectorAll('.counter');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const endValue = parseInt(target.getAttribute('data-value')) || 0;
                animateValue(target, 0, endValue, 2000);
                observer.unobserve(target);
            }
        });
    }, {
        threshold: 0.5
    });
    
    counterElements.forEach(element => {
        observer.observe(element);
    });
}

// Initialize counters if they exist
if (document.querySelector('.counter')) {
    document.addEventListener('DOMContentLoaded', initCounters);
}