// profesores.js - JavaScript para la aplicación appProfesores

document.addEventListener('DOMContentLoaded', function() {
    // Inicialización de editor de texto enriquecido si existe
    var contentEditor = document.querySelector('#id_contenido');
    if (contentEditor && typeof ClassicEditor !== 'undefined') {
        ClassicEditor
            .create(contentEditor)
            .catch(error => {
                console.error(error);
            });
    }
    
    // Preview de imagen de perfil
    var profileImageInput = document.querySelector('#id_foto');
    if (profileImageInput) {
        profileImageInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var imgPreview = document.querySelector('.img-preview');
                    if (imgPreview) {
                        imgPreview.src = e.target.result;
                    } else {
                        var placeholder = document.querySelector('.img-preview-placeholder');
                        if (placeholder) {
                            placeholder.innerHTML = '';
                            var img = document.createElement('img');
                            img.src = e.target.result;
                            img.classList.add('img-preview');
                            placeholder.appendChild(img);
                        }
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Confirmación para eliminar curso
    var confirmDeleteInput = document.getElementById('confirm-delete');
    var deleteButton = document.getElementById('delete-button');
    
    if (confirmDeleteInput && deleteButton) {
        confirmDeleteInput.addEventListener('input', function() {
            deleteButton.disabled = this.value !== 'ELIMINAR';
        });
    }
    
    // Filtro de cursos
    var courseSearch = document.querySelector('#course-search');
    if (courseSearch) {
        courseSearch.addEventListener('input', function() {
            var searchText = this.value.toLowerCase();
            var courseCards = document.querySelectorAll('.course-card');
            
            courseCards.forEach(function(card) {
                var title = card.querySelector('.course-title').textContent.toLowerCase();
                var description = card.querySelector('.course-description')?.textContent.toLowerCase() || '';
                
                if (title.includes(searchText) || description.includes(searchText)) {
                    card.closest('.col-md-6, .col-xl-4').style.display = 'block';
                } else {
                    card.closest('.col-md-6, .col-xl-4').style.display = 'none';
                }
            });
        });
    }
    
    // Filtro de estudiantes
    var studentSearch = document.querySelector('#student-search');
    if (studentSearch) {
        studentSearch.addEventListener('input', function() {
            var searchText = this.value.toLowerCase();
            var studentItems = document.querySelectorAll('.student-item');
            
            studentItems.forEach(function(item) {
                var name = item.querySelector('.student-name').textContent.toLowerCase();
                var email = item.querySelector('.student-email').textContent.toLowerCase();
                
                if (name.includes(searchText) || email.includes(searchText)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Toggle curso activo/inactivo
    var activeToggles = document.querySelectorAll('.active-toggle');
    if (activeToggles.length > 0) {
        activeToggles.forEach(function(toggle) {
            toggle.addEventListener('change', function() {
                var courseId = this.dataset.courseId;
                var active = this.checked;
                var statusBadge = document.querySelector(`.status-badge[data-course-id="${courseId}"]`);
                var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                fetch(`/profesores/cursos/${courseId}/toggle-active/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({active: active})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        if (active) {
                            statusBadge.textContent = 'Activo';
                            statusBadge.classList.remove('bg-secondary');
                            statusBadge.classList.add('bg-success');
                        } else {
                            statusBadge.textContent = 'Inactivo';
                            statusBadge.classList.remove('bg-success');
                            statusBadge.classList.add('bg-secondary');
                        }
                    }
                });
            });
        });
    }
});