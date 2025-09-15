// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on a nav link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
    
    // Sticky Navigation
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.padding = '10px 0';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.padding = '15px 0';
            navbar.style.boxShadow = 'none';
        }
    });
    
    // Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Testimonial Slider
    const testimonialSlider = document.querySelector('.testimonial-slider');
    if (testimonialSlider) {
        let isDown = false;
        let startX;
        let scrollLeft;
        
        testimonialSlider.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - testimonialSlider.offsetLeft;
            scrollLeft = testimonialSlider.scrollLeft;
        });
        
        testimonialSlider.addEventListener('mouseleave', () => {
            isDown = false;
        });
        
        testimonialSlider.addEventListener('mouseup', () => {
            isDown = false;
        });
        
        testimonialSlider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - testimonialSlider.offsetLeft;
            const walk = (x - startX) * 2;
            testimonialSlider.scrollLeft = scrollLeft - walk;
        });
        
        // Touch events for mobile
        testimonialSlider.addEventListener('touchstart', (e) => {
            isDown = true;
            startX = e.touches[0].pageX - testimonialSlider.offsetLeft;
            scrollLeft = testimonialSlider.scrollLeft;
        });
        
        testimonialSlider.addEventListener('touchend', () => {
            isDown = false;
        });
        
        testimonialSlider.addEventListener('touchmove', (e) => {
            if (!isDown) return;
            const x = e.touches[0].pageX - testimonialSlider.offsetLeft;
            const walk = (x - startX) * 2;
            testimonialSlider.scrollLeft = scrollLeft - walk;
        });
    }
    
    // Form Validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input[required], textarea[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Show error message
                let errorElement = this.querySelector('.error-message');
                if (!errorElement) {
                    errorElement = document.createElement('div');
                    errorElement.className = 'error-message';
                    errorElement.style.color = '#e74c3c';
                    errorElement.style.marginTop = '10px';
                    this.appendChild(errorElement);
                }
                errorElement.textContent = 'Please fill in all required fields.';
            }
        });
    });
    
    // Initialize animations
    initAnimations();
});

// Scroll Reveal Animations
function initAnimations() {
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOnScroll = () => {
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('active');
            }
        });
    };
    
    window.addEventListener('scroll', revealOnScroll);
    // Initial check
    revealOnScroll();
}

// Debounce function for performance
function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Scholarship Search and Filter
function initScholarshipFilters() {
    const searchInput = document.querySelector('.search-box input');
    const categoryFilter = document.querySelector('.filters select:first-child');
    const levelFilter = document.querySelector('.filters select:last-child');
    const scholarshipCards = document.querySelectorAll('.scholarship-card');
    
    if (!searchInput || !categoryFilter || !levelFilter) return;
    
    const filterScholarships = debounce(function() {
        const searchTerm = searchInput.value.toLowerCase();
        const categoryValue = categoryFilter.value;
        const levelValue = levelFilter.value;
        
        scholarshipCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const description = card.querySelector('.description').textContent.toLowerCase();
            const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent);
            
            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesCategory = categoryValue === 'All Categories' || tags.includes(categoryValue);
            const matchesLevel = levelValue === 'All Education Levels' || tags.includes(levelValue);
            
            if (matchesSearch && matchesCategory && matchesLevel) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }, 300);
    
    searchInput.addEventListener('input', filterScholarships);
    categoryFilter.addEventListener('change', filterScholarships);
    levelFilter.addEventListener('change', filterScholarships);
}

// Initialize when scholarships page loads
if (document.querySelector('.scholarships-grid')) {
    document.addEventListener('DOMContentLoaded', initScholarshipFilters);
}

