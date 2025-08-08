// Interactive features for Payment Splitter DApp Tutorial

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Smooth scrolling for anchor links
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
    
    // Code block copy functionality
    document.querySelectorAll('pre code').forEach(block => {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-primary copy-btn';
        button.textContent = 'Copy';
        button.style.position = 'absolute';
        button.style.top = '10px';
        button.style.right = '10px';
        
        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);
        
        button.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(block.textContent);
                button.textContent = 'Copied!';
                button.classList.remove('btn-outline-primary');
                button.classList.add('btn-success');
                
                setTimeout(() => {
                    button.textContent = 'Copy';
                    button.classList.remove('btn-success');
                    button.classList.add('btn-outline-primary');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy: ', err);
            }
        });
    });
    
    // Interactive progress bars
    document.querySelectorAll('.progress').forEach(progress => {
        const bar = progress.querySelector('.progress-bar');
        if (bar) {
            const width = bar.style.width;
            bar.style.width = '0%';
            
            setTimeout(() => {
                bar.style.transition = 'width 1s ease-in-out';
                bar.style.width = width;
            }, 500);
        }
    });
    
    // Collapsible sections
    document.querySelectorAll('.collapsible').forEach(section => {
        const trigger = section.querySelector('.collapsible-trigger');
        const content = section.querySelector('.collapsible-content');
        
        if (trigger && content) {
            trigger.addEventListener('click', () => {
                const isExpanded = content.style.display !== 'none';
                content.style.display = isExpanded ? 'none' : 'block';
                trigger.textContent = isExpanded ? 'Show' : 'Hide';
                trigger.classList.toggle('btn-outline-primary');
                trigger.classList.toggle('btn-primary');
            });
        }
    });
    
    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const sections = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
            
            sections.forEach(section => {
                const text = section.textContent.toLowerCase();
                if (text.includes(query)) {
                    section.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
                    section.scrollIntoView({ behavior: 'smooth', block: 'center' });
                } else {
                    section.style.backgroundColor = '';
                }
            });
        });
    }
    
    // Interactive code examples
    document.querySelectorAll('.interactive-code').forEach(example => {
        const runButton = example.querySelector('.run-code');
        const output = example.querySelector('.code-output');
        
        if (runButton && output) {
            runButton.addEventListener('click', () => {
                output.style.display = 'block';
                output.innerHTML = '<div class="alert alert-info">Running code example...</div>';
                
                // Simulate code execution
                setTimeout(() => {
                    output.innerHTML = `
                        <div class="alert alert-success">
                            <strong>Success!</strong> Code executed successfully.
                            <br>Output: Payment created with ID: 1
                        </div>
                    `;
                }, 1000);
            });
        }
    });
    
    // Table of contents highlighting
    const toc = document.querySelector('.toc');
    if (toc) {
        const tocLinks = toc.querySelectorAll('a');
        const sections = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        
        window.addEventListener('scroll', () => {
            let current = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });
            
            tocLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                }
            });
        });
    }
    
    // Dark mode toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark);
            
            darkModeToggle.textContent = isDark ? '☀️ Light' : '🌙 Dark';
        });
        
        // Check for saved preference
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'true') {
            document.body.classList.add('dark-mode');
            darkModeToggle.textContent = '☀️ Light';
        }
    }
    
    // Interactive diagrams
    document.querySelectorAll('.interactive-diagram').forEach(diagram => {
        const canvas = diagram.querySelector('canvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            
            // Draw blockchain diagram
            ctx.fillStyle = '#667eea';
            ctx.fillRect(10, 10, 80, 40);
            ctx.fillStyle = 'white';
            ctx.font = '12px Arial';
            ctx.fillText('Block', 30, 35);
            
            ctx.fillStyle = '#764ba2';
            ctx.fillRect(110, 10, 80, 40);
            ctx.fillStyle = 'white';
            ctx.fillText('Block', 130, 35);
            
            ctx.fillStyle = '#667eea';
            ctx.fillRect(210, 10, 80, 40);
            ctx.fillStyle = 'white';
            ctx.fillText('Block', 230, 35);
        }
    });
    
    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Auto-save form data
    document.querySelectorAll('input, textarea').forEach(input => {
        const key = 'form_' + input.name;
        
        // Load saved data
        const saved = localStorage.getItem(key);
        if (saved) {
            input.value = saved;
        }
        
        // Save on input
        input.addEventListener('input', function() {
            localStorage.setItem(key, this.value);
        });
    });
    
    // Print functionality
    const printButton = document.getElementById('print-button');
    if (printButton) {
        printButton.addEventListener('click', () => {
            window.print();
        });
    }
    
    // Share functionality
    const shareButton = document.getElementById('share-button');
    if (shareButton) {
        shareButton.addEventListener('click', () => {
            if (navigator.share) {
                navigator.share({
                    title: 'Payment Splitter DApp Tutorial',
                    text: 'Learn to build blockchain applications for Ugandan developers',
                    url: window.location.href
                });
            } else {
                // Fallback: copy URL to clipboard
                navigator.clipboard.writeText(window.location.href);
                alert('URL copied to clipboard!');
            }
        });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Ctrl/Cmd + P for print
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            window.print();
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
    
    // Performance monitoring
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Send analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', 'page_view', {
                page_title: document.title,
                page_location: window.location.href,
                load_time: loadTime
            });
        }
    });
    
    // Accessibility improvements
    document.querySelectorAll('button, a').forEach(element => {
        if (!element.hasAttribute('aria-label') && !element.textContent.trim()) {
            element.setAttribute('aria-label', element.title || 'Interactive element');
        }
    });
    
    // Focus management
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Console welcome message
    console.log(`
    🚀 Welcome to the Payment Splitter DApp Tutorial!
    
    🇺🇬 Built with ❤️ for the Ugandan Web3 community
    
    📚 This tutorial teaches you:
    - Smart contract development with Solidity
    - Blockchain deployment on Celo
    - Web3 integration with Python
    - Modern web development with Flask
    
    🎯 Ready to build something amazing? Let's go!
    `);
    
});
