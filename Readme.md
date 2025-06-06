# 🌍 Aprende Español - Plataforma de Aprendizaje con Django  

**Descripción**:  
Aplicación web desarrollada con **Django** para enseñar español de manera interactiva. Incluye lecciones, ejercicios prácticos, quizzes y seguimiento del progreso del usuario.  

---  

## 🛠 Stack Tecnológico  
| **Frontend**  | **Backend**       | **Base de Datos** | **Herramientas**      |  
|---------------|-------------------|-------------------|-----------------------|  
| HTML5         | Python + Django   | PostgreSQL        | Git + GitHub          |  
| CSS3          | Django REST       | SQLite (dev)      | Figma (diseño)        |  
| JavaScript    |                   |                   | VS Code               |  

---  

## ✨ Características Principales  
✅ **Autenticación de usuarios**: Registro, login y recuperación de contraseña.  
✅ **Lecciones por niveles**: Desde básico (A1) hasta avanzado (C1).  
✅ **Ejercicios interactivos**:  
   - Flashcards de vocabulario.  
   - Quizzes con retroalimentación instantánea.  
   - Grabaciones para practicar pronunciación (usando Web API de JS).  
✅ **Panel de progreso**: Gráficos y estadísticas de aprendizaje.  
✅ **Diseño responsive**: Compatible con móviles y tablets.  

---  

## 🚀 Instalación Local  
1. **Clona el repositorio**:  
   ```bash  
   git clone https://github.com/tu-usuario/aprende-espanol.git  
   cd aprende-espanol  
   ```  

2. **Crea un entorno virtual (recomendado)**:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # Linux/Mac  
   venv\Scripts\activate     # Windows  
   ```  

3. **Instala dependencias**:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Configura la base de datos**:  
   ```bash  
   python manage.py migrate  
   ```  

5. **Ejecuta el servidor de desarrollo**:  
   ```bash  
   python manage.py runserver  
   ```  
   Abre tu navegador en: [http://127.0.0.1:8000](http://127.0.0.1:8000).  

---  

## 📂 Estructura del Proyecto (key files)  
```  
aprende-espanol/  
├── core/                  # App principal de Django  
│   ├── models.py          # Modelos de usuarios/lecciones  
│   ├── views.py           # Lógica de las vistas  
│   └── templates/         # HTML base  
├── static/                # CSS, JS, imágenes  
├── media/                 # Archivos subidos por usuarios  
├── requirements.txt       # Dependencias de Python  
└── manage.py              # Script de administración  
```  

---  

## 🌟 Cómo Contribuir  
1. Haz un **fork** del proyecto.  
2. Crea una rama:  
   ```bash  
   git checkout -b fix/nombre-del-fix  
   ```  
3. Sube tus cambios:  
   ```bash  
   git push origin fix/nombre-del-fix  
   ```  
4. Abre un **Pull Request** en GitHub.  

---  

## 📄 Licencia  
MIT License. Ver archivo [LICENSE](LICENSE).  

---  

## ✉️ Contacto  
¿Dudas o sugerencias? ¡Escríbeme!  
- 📧 Email: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)  
- 🔗 LinkedIn: [Tu Nombre](https://linkedin.com/in/tu-perfil)  

---  

### 📌 Capturas de Pantalla (opcional)  
Si quieres, agrega imágenes como esta:  
![Home](static/images/screenshot-home.png) *Página de inicio*  

---  
