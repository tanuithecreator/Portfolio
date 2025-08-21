// DOM Elements
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const contactForm = document.getElementById('contact-form');
const filterBtns = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');
const statNumbers = document.querySelectorAll('.stat-number');

// Mobile Navigation Toggle
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Navbar scroll effect and active link highlighting
window.addEventListener('scroll', () => {
    // Navbar background change
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

    // Active link highlighting
    const sections = document.querySelectorAll('section');
    const scrollPos = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');

        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});

// Smooth scrolling for navigation links
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            const offsetTop = targetSection.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Project filtering
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        filterBtns.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');

        const filterValue = btn.getAttribute('data-filter');

        projectCards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');
            
            if (filterValue === 'all' || cardCategory === filterValue) {
                card.style.display = 'block';
                card.style.animation = 'fadeIn 0.5s ease-in-out';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

// Animated counter for statistics
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);

    const timer = setInterval(() => {
        start += increment;
        element.textContent = Math.floor(start);

        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        }
    }, 16);
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.3,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Animate statistics counters
            if (entry.target.classList.contains('stats')) {
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.getAttribute('data-target'));
                    animateCounter(stat, target);
                });
            }

            // Add animation classes
            if (entry.target.classList.contains('skill-category')) {
                entry.target.style.animation = 'slideInUp 0.8s ease-out';
            }

            if (entry.target.classList.contains('project-card')) {
                entry.target.style.animation = 'slideInUp 0.8s ease-out';
            }

            if (entry.target.classList.contains('about-text')) {
                entry.target.style.animation = 'slideInLeft 1s ease-out';
            }

            if (entry.target.classList.contains('about-image')) {
                entry.target.style.animation = 'slideInRight 1s ease-out';
            }

            // Unobserve after animation
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.skill-category, .project-card, .stats, .about-text, .about-image');
    animatedElements.forEach(el => observer.observe(el));
});

// Contact form functionality
const formGroups = document.querySelectorAll('.form-group');

// Enhanced form styling and validation
formGroups.forEach(group => {
    const input = group.querySelector('input, textarea');
    
    if (input) {
        // Focus and blur effects
        input.addEventListener('focus', () => {
            group.classList.add('focused');
        });

        input.addEventListener('blur', () => {
            if (input.value.trim() === '') {
                group.classList.remove('focused');
                group.classList.remove('filled');
            } else {
                group.classList.add('filled');
            }
        });

        // Real-time validation styling
        input.addEventListener('input', () => {
            if (input.value.trim() !== '') {
                group.classList.add('filled');
            } else {
                group.classList.remove('filled');
            }

            // Email validation
            if (input.type === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (emailRegex.test(input.value)) {
                    input.style.borderColor = '#10b981';
                } else if (input.value.length > 0) {
                    input.style.borderColor = '#ef4444';
                } else {
                    input.style.borderColor = '';
                }
            }
        });
    }
});

// Contact form submission
contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = contactForm.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('span');
    const btnIcon = submitBtn.querySelector('i');
    
    // Get form data
    const formData = new FormData(contactForm);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        subject: formData.get('subject'),
        message: formData.get('message')
    };

    // Basic validation
    if (!data.name || !data.email || !data.subject || !data.message) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }

    // Loading state
    submitBtn.classList.add('loading');
    btnText.textContent = 'Sending...';
    btnIcon.className = 'fas fa-spinner';

    try {
        // Simulate form submission (replace with actual endpoint)
        await simulateFormSubmission(data);
        
        // Success state
        showNotification('Message sent successfully! I\'ll get back to you soon.', 'success');
        contactForm.reset();
        
        // Reset form groups
        formGroups.forEach(group => {
            group.classList.remove('focused', 'filled');
        });

    } catch (error) {
        showNotification('Oops! Something went wrong. Please try again.', 'error');
    } finally {
        // Reset button state
        submitBtn.classList.remove('loading');
        btnText.textContent = 'Send Message';
        btnIcon.className = 'fas fa-paper-plane';
    }
});

// Simulate form submission (replace with actual API call)
function simulateFormSubmission(data) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simulate success/failure
            if (Math.random() > 0.1) {
                resolve(data);
            } else {
                reject(new Error('Network error'));
            }
        }, 2000);
    });
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 400px;
        animation: slideInRight 0.3s ease forwards;
    `;

    // Add to DOM
    document.body.appendChild(notification);

    // Close functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Typing effect for hero section
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typing effect
document.addEventListener('DOMContentLoaded', () => {
    const typingElement = document.querySelector('.typing-text');
    if (typingElement) {
        // Remove the CSS animation cursor
        typingElement.style.setProperty('--cursor', 'none');
        
        setTimeout(() => {
            typeWriter(typingElement, 'Your Name', 150);
        }, 1000);
    }
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.bg-animation');
    
    parallaxElements.forEach(element => {
        const speed = 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Smooth reveal animations for sections
const revealElements = document.querySelectorAll('section > *');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

// Initialize reveal animations
document.addEventListener('DOMContentLoaded', () => {
    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        revealObserver.observe(el);
    });
});

// Add custom cursor effect (optional)
function createCustomCursor() {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    cursor.style.cssText = `
        position: fixed;
        width: 20px;
        height: 20px;
        background: var(--primary-color);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        opacity: 0;
        transition: all 0.1s ease;
        mix-blend-mode: difference;
    `;
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX - 10 + 'px';
        cursor.style.top = e.clientY - 10 + 'px';
        cursor.style.opacity = '1';
    });

    document.addEventListener('mouseleave', () => {
        cursor.style.opacity = '0';
    });

    // Scale effect on hover
    const hoverElements = document.querySelectorAll('a, button, .project-card, .skill-item');
    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.style.transform = 'scale(2)';
        });
        el.addEventListener('mouseleave', () => {
            cursor.style.transform = 'scale(1)';
        });
    });
}

// Initialize custom cursor (uncomment if desired)
// createCustomCursor();

// Performance optimization: Throttle scroll events
function throttle(func, wait) {
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

// Apply throttling to scroll events
const throttledScrollHandler = throttle(() => {
    // Your scroll handler code here
}, 16); // ~60fps

// Error handling
window.addEventListener('error', (e) => {
    console.error('An error occurred:', e.error);
});

// Loading animation
document.addEventListener('DOMContentLoaded', () => {
    // Hide loading spinner if you have one
    const loader = document.querySelector('.loader');
    if (loader) {
        setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => loader.remove(), 300);
        }, 1000);
    }
});

console.log('🚀 Portfolio loaded successfully!');