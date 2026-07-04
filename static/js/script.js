// ===== DOM Ready =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🕵️ Mobile Phone OSINT Tool Loaded');
    
    // ===== Create Particle Background =====
    createParticles();
    
    // ===== Input Validation =====
    const phoneInput = document.querySelector('.search-input');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            // Auto-format: remove non-numeric except '+'
            let value = this.value.replace(/[^\d+]/g, '');
            this.value = value;
            
            // Visual feedback
            if (value.length > 3) {
                this.style.borderColor = 'rgba(0, 240, 255, 0.6)';
                this.style.boxShadow = '0 0 30px rgba(0, 240, 255, 0.1)';
            } else if (value.length > 0) {
                this.style.borderColor = 'rgba(255, 200, 0, 0.4)';
            } else {
                this.style.borderColor = 'rgba(0, 240, 255, 0.2)';
                this.style.boxShadow = 'none';
            }
        });
        
        // Auto-focus
        phoneInput.focus();
    }
    
    // ===== Smooth Scrolling for Results =====
    const resultsSection = document.querySelector('.result-card');
    if (resultsSection) {
        setTimeout(() => {
            resultsSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 300);
    }
});

// ===== Create Particle Background =====
function createParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    document.body.prepend(particlesContainer);
    
    const colors = ['#00f0ff', '#7c4dff', '#ff6b6b', '#00ff64', '#ffc800'];
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        const size = Math.random() * 4 + 2;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (Math.random() * 20 + 15) + 's';
        particle.style.animationDelay = (Math.random() * 20) + 's';
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        particle.style.opacity = Math.random() * 0.3 + 0.1;
        particlesContainer.appendChild(particle);
    }
}

// ===== Copy Phone Number to Clipboard =====
function copyPhoneNumber(phone) {
    navigator.clipboard.writeText(phone).then(() => {
        showToast('📋 Phone number copied!');
    }).catch(() => {
        showToast('❌ Failed to copy');
    });
}

// ===== Toast Notification =====
function showToast(message) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        color: #fff;
        padding: 15px 30px;
        border-radius: 15px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
        z-index: 9999;
        animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}