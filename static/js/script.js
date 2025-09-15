// Enhanced JavaScript for Vidhyasathi Scholarship Platform

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initStepAnimations();
    initBackToTop();
    initNavbar();
    initAnimations();
    initForms();
    initFilterSystem();
    initForumInteractions();
    initTestimonialSlider();
    
    // Add any additional initialization here
    console.log('Vidhyasathi platform initialized');
});



// Navbar functionality
function initNavbar() {
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
        link.addEventListener('click', function() {
            if (navMenu.classList.contains('active')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.padding = '0.5rem 0';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.padding = '1rem 0';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.05)';
        }
    });
    
    // Close alerts
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
}
// Floating cards animation
            const floatingCards = document.querySelectorAll('.floating-card');
            floatingCards.forEach(card => {
                card.addEventListener('mouseenter', () => {
                    card.style.animationPlayState = 'paused';
                });
                
                card.addEventListener('mouseleave', () => {
                    card.style.animationPlayState = 'running';
                });
            });
            

// Animation initialization
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animatedElements = document.querySelectorAll('.feature-card, .step, .testimonial-card, .scholarship-card');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
    
    // Add animated class to hero elements
    const heroElements = document.querySelectorAll('.hero h1, .hero p, .hero-buttons');
    heroElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.2}s`;
    });
}
// Initialize step animations
function initStepAnimations() {
    const steps = document.querySelectorAll('.step');
    const stepsObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('step-visible');
                }, index * 200);
            }
        });
    }, { threshold: 0.3 });
    
    steps.forEach(step => {
        stepsObserver.observe(step);
    });
}

// Back to top button functionality
function initBackToTop() {
    const backToTop = document.createElement('a');
    backToTop.href = '#';
    backToTop.className = 'back-to-top';
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });
    
    backToTop.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Form handling
function initForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Basic form validation
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    highlightField(field, false);
                } else {
                    highlightField(field, true);
                }
            });
            
            // Password confirmation check
            const password = form.querySelector('#password');
            const confirmPassword = form.querySelector('#confirm-password');
            
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                isValid = false;
                highlightField(confirmPassword, false);
                showNotification('Passwords do not match', 'error');
            }
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly', 'error');
            }
        });
    });
    
    // Input validation on blur
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                highlightField(this, false);
            } else {
                highlightField(this, true);
            }
        });
        
        // Clear validation on input
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                highlightField(this, true);
            }
        });
    });
    
    // Password visibility toggle
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    });
}

// Field highlighting
function highlightField(field, isValid) {
    if (isValid) {
        field.style.borderColor = '#4cc9f0';
    } else {
        field.style.borderColor = '#f94144';
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="alert-close">&times;</button>
    `;
    
    // Add to messages container
    const messagesContainer = document.querySelector('.messages-container');
    if (messagesContainer) {
        messagesContainer.appendChild(notification);
    } else {
        // Create messages container if it doesn't exist
        const container = document.createElement('div');
        container.className = 'messages-container';
        container.appendChild(notification);
        document.body.appendChild(container);
    }
    
    // Close button event
    const closeButton = notification.querySelector('.alert-close');
    closeButton.addEventListener('click', function() {
        notification.style.display = 'none';
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.display = 'none';
        }
    }, 5000);
}

// Scholarship filter system
function initFilterSystem() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const categoryFilter = document.getElementById('category-filter');
    const educationFilter = document.getElementById('education-filter');
    const scholarshipCards = document.querySelectorAll('.scholarship-card');
    
    // Search functionality
    if (searchInput && searchButton) {
        searchButton.addEventListener('click', function() {
            filterScholarships();
        });
        
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                filterScholarships();
            }
        });
    }
    
    // Filter functionality
    if (categoryFilter && educationFilter) {
        categoryFilter.addEventListener('change', filterScholarships);
        educationFilter.addEventListener('change', filterScholarships);
    }
    
    function filterScholarships() {
        const searchText = searchInput ? searchInput.value.toLowerCase() : '';
        const categoryValue = categoryFilter ? categoryFilter.value : 'all';
        const educationValue = educationFilter ? educationFilter.value : 'all';
        
        scholarshipCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const description = card.querySelector('.description').textContent.toLowerCase();
            const type = card.getAttribute('data-type');
            const education = card.getAttribute('data-education');
            
            const matchesSearch = searchText === '' || title.includes(searchText) || description.includes(searchText);
            const matchesCategory = categoryValue === 'all' || type === categoryValue;
            const matchesEducation = educationValue === 'all' || education === educationValue;
            
            if (matchesSearch && matchesCategory && matchesEducation) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
}

// Forum interactions
function initForumInteractions() {
    // Add any forum-specific interactions here
}

// Testimonial slider
function initTestimonialSlider() {
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
    }
}

// Additional utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global access if needed
window.Vidhyasathi = {
    showNotification,
    debounce
};

