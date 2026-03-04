// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
});

// Initialize features on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            mobileMenu.classList.toggle('hidden');
        });

        // Close mobile menu when a link is clicked
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }

    // Observe all glass cards for scroll animation
    document.querySelectorAll('.glass-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// AI Agent Modal Logic
const aiModal = document.getElementById('ai-modal');
const closeAiModal = document.getElementById('close-ai-modal');
const tryAiBtn = document.getElementById('try-ai-btn');
const aiChatForm = document.getElementById('ai-chat-form');
const aiInput = document.getElementById('ai-input');
const aiChatBody = document.getElementById('ai-chat-body');

const openAiAgent = () => {
    aiModal.classList.remove('hidden');
    aiModal.classList.add('flex');
    document.body.classList.add('overflow-hidden');
};

const closeAiAgent = () => {
    aiModal.classList.add('hidden');
    aiModal.classList.remove('flex');
    document.body.classList.remove('overflow-hidden');
};

if (tryAiBtn) tryAiBtn.addEventListener('click', openAiAgent);
if (closeAiModal) closeAiModal.addEventListener('click', closeAiAgent);

if (aiChatForm) {
    aiChatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = aiInput.value.trim();
        if (!text) return;

        // Add user message
        addChatMessage(text, 'user');
        aiInput.value = '';

        // Mock AI response
        setTimeout(() => {
            const responses = [
                "That's an interesting question about African AI research!",
                "NAIRA focuses on embedding local culture into technology.",
                "Our XR classrooms are being piloted in major Nigerian universities.",
                "How can I help you with our strategic pillars today?",
                "We are working on LLMs specifically for Yoruba, Igbo, and Hausa."
            ];
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            addChatMessage(randomResponse, 'ai');
        }, 800);
    });
}

function addChatMessage(text, sender) {
    const div = document.createElement('div');
    div.className = sender === 'user' ? 'flex justify-end' : 'flex items-start gap-3';

    if (sender === 'user') {
        div.innerHTML = `
            <div class="bg-indigo-600 rounded-2xl rounded-tr-none p-3 text-sm text-white max-w-[80%]">
                ${text}
            </div>
        `;
    } else {
        div.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-indigo-600/20 flex items-center justify-center shrink-0">
                <i data-feather="cpu" class="w-4 h-4 text-indigo-400"></i>
            </div>
            <div class="bg-white/5 border border-white/10 rounded-2xl rounded-tl-none p-3 text-sm text-slate-300 max-w-[80%]">
                ${text}
            </div>
        `;
    }

    aiChatBody.appendChild(div);
    feather.replace();
    aiChatBody.scrollTop = aiChatBody.scrollHeight;
}

// Dark/Light Mode Logic
const themeToggle = document.getElementById('theme-toggle');
const themeToggleMobile = document.getElementById('theme-toggle-mobile');
const themeIconDark = document.getElementById('theme-icon-dark');
const themeIconLight = document.getElementById('theme-icon-light');

const applyTheme = (theme) => {
    if (theme === 'light') {
        document.documentElement.classList.add('light-mode');
        if (themeIconDark) themeIconDark.classList.add('hidden');
        if (themeIconLight) themeIconLight.classList.remove('hidden');
    } else {
        document.documentElement.classList.remove('light-mode');
        if (themeIconDark) themeIconDark.classList.remove('hidden');
        if (themeIconLight) themeIconLight.classList.add('hidden');
    }
};

const toggleTheme = () => {
    const currentTheme = document.documentElement.classList.contains('light-mode') ? 'light' : 'dark';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
};

if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
if (themeToggleMobile) themeToggleMobile.addEventListener('click', toggleTheme);

// Initialize theme from localStorage
const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
applyTheme(savedTheme);

// Multilingual Logic
const translations = {
    'en': {
        'nav-home': 'Home',
        'nav-vision': 'Vision',
        'nav-pillars': 'Pillars',
        'nav-architecture': 'Architecture',
        'nav-revenue': 'Revenue',
        'nav-content': 'Content',
        'nav-projects': 'Projects',
        'hero-title': 'NAIRA',
        'hero-badge': "Pioneering Africa's AI Renaissance",
        'hero-subtitle': 'NBU ARTIFICIAL INTELLIGENCE RESEARCH & ADVANCEMENT INSTITUTE',
        'hero-description': 'Transforming education and innovation through immersive XR experiences and agentic AI architectures, embedding African languages, culture, and indigenous knowledge into global technology solutions.'
    },
    'yo': {
        'nav-home': 'Ile',
        'nav-vision': 'Iriran',
        'nav-pillars': 'Awọn Opó',
        'nav-architecture': 'Imọ-iṣelọpọ',
        'nav-revenue': 'Owo-wiwọle',
        'nav-content': 'Àkóónú',
        'nav-projects': 'Awọn Ise-Agbeṣe',
        'hero-title': 'NAIRA',
        'hero-badge': "Asiwaju Isọji AI ti Afirika",
        'hero-subtitle': 'ILE-IṢẸ NBU FUN IWADII ATI ILỌSIWAJU AI',
        'hero-description': 'Yiyipada eto ẹkọ ati isọdọtun nipasẹ awọn iriri XR immersive ati awọn faaji AI aṣoju, fifi awọn ede Afirika, aṣa, ati imọ abinibi sinu awọn ojutu imọ-ẹrọ agbaye.'
    },
    'sw': {
        'nav-home': 'Nyumbani',
        'nav-vision': 'Maono',
        'nav-pillars': 'Nguzo',
        'nav-architecture': 'Usanifu',
        'nav-revenue': 'Mapato',
        'nav-content': 'Maudhui',
        'nav-projects': 'Miradi',
        'hero-title': 'NAIRA',
        'hero-badge': "Uanzilishi wa Renaissance ya AI ya Afrika",
        'hero-subtitle': 'TAASISI YA NBU YA UTAFITI NA MAENDELEO YA AI',
        'hero-description': 'Kubadilisha elimu na uvumbuzi kupitia uzoefu wa XR wa kuzama na usanifu wa AI, kupachika lugha za Kiafrika, utamaduni, na maarifa asilia katika suluhisho za teknolojia ya kimataifa.'
    }
};

window.switchLang = (lang) => {
    localStorage.setItem('lang', lang);
    applyLang(lang);
};

const applyLang = (lang) => {
    const langStrings = translations[lang] || translations['en'];
    document.querySelectorAll('[data-key]').forEach(el => {
        const key = el.getAttribute('data-key');
        if (langStrings[key]) {
            el.textContent = langStrings[key];
        }
    });

    // Specifically handle hero elements if they exist on the page
    const heroTitle = document.getElementById('hero-title');
    const heroBadge = document.getElementById('hero-badge');
    const heroSubtitle = document.getElementById('hero-subtitle');
    const heroDescription = document.getElementById('hero-description');

    if (heroTitle && langStrings['hero-title']) heroTitle.textContent = langStrings['hero-title'];
    if (heroBadge && langStrings['hero-badge']) heroBadge.textContent = langStrings['hero-badge'];
    if (heroSubtitle && langStrings['hero-subtitle']) heroSubtitle.textContent = langStrings['hero-subtitle'];
    if (heroDescription && langStrings['hero-description']) heroDescription.textContent = langStrings['hero-description'];

    const langDisplay = document.getElementById('current-lang');
    if (langDisplay) langDisplay.textContent = lang.toUpperCase();
};

// Initialize language from localStorage
const savedLang = localStorage.getItem('lang') || 'en';
applyLang(savedLang);

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
const handleNewsletterSubmit = async (form, statusEl) => {
    const formData = new FormData(form);
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
        statusEl.classList.remove('hidden');
        if (result.success) {
            statusEl.className = 'text-center py-2 px-4 rounded-xl mt-3 bg-emerald-600/20 text-emerald-400 border border-emerald-500/30';
            statusEl.textContent = result.message;
            form.reset();
        } else {
            statusEl.className = 'text-center py-2 px-4 rounded-xl mt-3 bg-amber-600/20 text-amber-400 border border-amber-500/30';
            statusEl.textContent = result.message;
        }
        setTimeout(() => {
            statusEl.classList.add('hidden');
        }, 5000);
    } catch (error) {
        statusEl.classList.remove('hidden');
        statusEl.className = 'text-center py-2 px-4 rounded-xl mt-3 bg-red-600/20 text-red-400 border border-red-500/30';
        statusEl.textContent = 'Network error. Please try again.';
    }
};

const newsletterForm = document.getElementById('newsletter-form');
const newsletterStatus = document.getElementById('newsletter-status');
if (newsletterForm && newsletterStatus) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleNewsletterSubmit(newsletterForm, newsletterStatus);
    });
}

const newsletterFormHome = document.getElementById('newsletter-form-home');
const newsletterStatusHome = document.getElementById('newsletter-status-home');
if (newsletterFormHome && newsletterStatusHome) {
    newsletterFormHome.addEventListener('submit', (e) => {
        e.preventDefault();
        handleNewsletterSubmit(newsletterFormHome, newsletterStatusHome);
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
