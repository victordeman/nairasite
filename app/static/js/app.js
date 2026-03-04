// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
});
// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
    // Close mobile menu when a link is clicked
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });
}
// Contact Form Submission
const contactForm = document.getElementById('contact-form');
const contactStatus = document.getElementById('contact-status');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(contactForm);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            role: formData.get('role') || '',
            message: formData.get('message'),
        };
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            contactStatus.classList.remove('hidden');
            if (result.success) {
                contactStatus.className = 'text-center py-3 px-4 rounded-xl bg-emerald-600/20 text-emerald-400 border border-emerald-500/30';
                contactStatus.textContent = result.message;
                contactForm.reset();
            } else {
                contactStatus.className = 'text-center py-3 px-4 rounded-xl bg-red-600/20 text-red-400 border border-red-500/30';
                contactStatus.textContent = result.message || 'Something went wrong. Please try again.';
            }
            setTimeout(() => {
                contactStatus.classList.add('hidden');
            }, 5000);
        } catch (error) {
            contactStatus.classList.remove('hidden');
            contactStatus.className = 'text-center py-3 px-4 rounded-xl bg-red-600/20 text-red-400 border border-red-500/30';
            contactStatus.textContent = 'Network error. Please try again.';
        }
    });
}
// Newsletter Form Submission
const newsletterForm = document.getElementById('newsletter-form');
const newsletterStatus = document.getElementById('newsletter-status');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(newsletterForm);
        const data = {
            email: formData.get('email'),
        };
        try {
            const response = await fetch('/api/newsletter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            newsletterStatus.classList.remove('hidden');
            if (result.success) {
                newsletterStatus.className = 'text-center py-2 px-4 rounded-xl mt-3 bg-emerald-600/20 text-emerald-400 border border-emerald-500/30';
                newsletterStatus.textContent = result.message;
                newsletterForm.reset();
            } else {
                newsletterStatus.className = 'text-center py-2 px-4 rounded-xl mt-3 bg-amber-600/20 text-amber-400 border border-amber-500/30';
                newsletterStatus.textContent = result.message;
            }
            setTimeout(() => {
                newsletterStatus.classList.add('hidden');
            }, 5000);
        } catch (error) {
            newsletterStatus.classList.remove('hidden');
            newsletterStatus.className = 'text-center py-2 px-4 rounded-xl mt-3 bg-red-600/20 text-red-400 border border-red-500/30';
            newsletterStatus.textContent = 'Network error. Please try again.';
        }
    });
}
// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);
// Observe all glass cards for scroll animation
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.glass-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});
