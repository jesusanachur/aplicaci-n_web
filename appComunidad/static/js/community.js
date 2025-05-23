// community.js - JavaScript para la aplicación appComunidad

document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidad para el carrusel de testimonios si existe
    var testimonialCarousel = document.querySelector('#testimonialCarousel');
    if (testimonialCarousel) {
        var carousel = new bootstrap.Carousel(testimonialCarousel, {
            interval: 5000,
            touch: true
        });
    }
    
    // Animación para los contadores de estadísticas si existen
    var counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        counters.forEach(function(counter) {
            var target = parseInt(counter.getAttribute('data-target'));
            var count = 0;
            var interval = setInterval(function() {
                if (count < target) {
                    count += Math.ceil(target / 100);
                    if (count > target) count = target;
                    counter.innerText = count;
                } else {
                    clearInterval(interval);
                }
            }, 30);
        });
    }
    
    // Funcionalidad para el filtro de noticias si existe
    var newsFilter = document.querySelector('#newsFilter');
    if (newsFilter) {
        newsFilter.addEventListener('change', function() {
            var category = this.value;
            var newsItems = document.querySelectorAll('.news-item');
            
            if (category === 'all') {
                newsItems.forEach(function(item) {
                    item.style.display = 'block';
                });
            } else {
                newsItems.forEach(function(item) {
                    if (item.getAttribute('data-category') === category) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            }
        });
    }
    
    // Validación del formulario de contacto si existe
    var contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            var valid = true;
            
            // Validación simple de campos requeridos
            contactForm.querySelectorAll('[required]').forEach(function(field) {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            // Validación de email
            var emailField = contactForm.querySelector('[type="email"]');
            if (emailField && emailField.value.trim()) {
                var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    valid = false;
                    emailField.classList.add('is-invalid');
                }
            }
            
            if (!valid) {
                event.preventDefault();
            }
        });
    }
});