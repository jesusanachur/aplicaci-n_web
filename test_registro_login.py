from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string

def generar_usuario_aleatorio():
    """Genera un nombre de usuario aleatorio"""
    return f"testuser_{''.join(random.choices(string.ascii_lowercase, k=6))}"

def generar_correo_aleatorio():
    """Genera un correo electrónico aleatorio"""
    return f"{''.join(random.choices(string.ascii_lowercase, k=8))}@test.com"

def configurar_navegador():
    """Configura y devuelve una instancia del navegador Chrome"""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("start-maximized")  # Maximiza la ventana del navegador
    opciones.add_argument("--disable-gpu")  # Desactiva la aceleración por hardware
    opciones.add_argument("--incognito")  # Modo incógnito
    # opciones.add_argument("--headless")  # Descomentar para modo sin interfaz gráfica
    
    # Configurar el servicio de Chrome
    servicio = Service(ChromeDriverManager().install())
    
    # Crear y devolver la instancia del navegador
    navegador = webdriver.Chrome(service=servicio, options=opciones)
    return navegador

def registrar_estudiante(driver, usuario, correo, contrasena, nombre="Test", apellido="User"):
    """
    Registra un nuevo estudiante en la aplicación
    
    Args:
        driver: Instancia del navegador
        usuario (str): Nombre de usuario
        correo (str): Correo electrónico
        contrasena (str): Contraseña
        nombre (str): Nombre del usuario (opcional, por defecto "Test")
        apellido (str): Apellido del usuario (opcional, por defecto "User")
    """
    try:
        # Navegar a la página de registro de estudiante
        driver.get("http://127.0.0.1:8000/register/student/")
        print(f"[INFO] Accediendo a la página de registro de estudiante...")
        
        # Esperar a que el formulario esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Tomar captura antes de llenar el formulario
        driver.save_screenshot("antes_del_registro.png")
        
        # Llenar el formulario de registro
        driver.find_element(By.NAME, "username").send_keys(usuario)
        driver.find_element(By.NAME, "first_name").send_keys(nombre)
        driver.find_element(By.NAME, "last_name").send_keys(apellido)
        driver.find_element(By.NAME, "email").send_keys(correo)
        driver.find_element(By.NAME, "password1").send_keys(contrasena)
        driver.find_element(By.NAME, "password2").send_keys(contrasena)
        
        # Tomar captura después de llenar el formulario
        driver.save_screenshot("formulario_llenado.png")
        
        # Hacer clic en el botón de registro
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Esperar a que se complete el registro
        time.sleep(2)
        
        # Verificar si el registro fue exitoso
        if "login" in driver.current_url or "accounts/profile" in driver.current_url:
            print("[INFO] Registro exitoso")
            driver.save_screenshot("registro_exitoso.png")
            return True
        else:
            # Verificar si hay mensajes de error
            try:
                error_messages = driver.find_elements(By.CLASS_NAME, "error")
                if error_messages:
                    print(f"[ERROR] Error en el registro: {error_messages[0].text}")
            except:
                pass
            
            driver.save_screenshot("error_registro.png")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error durante el registro: {str(e)}")
        driver.save_screenshot("error_registro.png")
        return False

def iniciar_sesion(driver, usuario, contrasena):
    """
    Inicia sesión en la aplicación con las credenciales proporcionadas
    
    Args:
        driver: Instancia del navegador
        usuario (str): Nombre de usuario o correo
        contrasena (str): Contraseña
    """
    try:
        # Navegar a la página de inicio de sesión
        driver.get("http://127.0.0.1:8000/login/")
        print(f"\n[INFO] Accediendo a la página de inicio de sesión...")
        
        # Esperar a que el formulario esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Tomar captura antes de llenar el formulario
        driver.save_screenshot("antes_del_login.png")
        
        # Llenar el formulario
        driver.find_element(By.NAME, "username").send_keys(usuario)
        driver.find_element(By.NAME, "password").send_keys(contrasena)
        
        # Hacer clic en el botón de inicio de sesión
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Esperar a que se complete el inicio de sesión
        time.sleep(2)
        
        # Verificar si el inicio de sesión fue exitoso
        if "login" not in driver.current_url:
            print("[INFO] Inicio de sesión exitoso")
            driver.save_screenshot("inicio_sesion_exitoso.png")
            return True
        else:
            # Verificar si hay mensajes de error
            try:
                error_message = driver.find_element(By.CLASS_NAME, "error").text
                print(f"[ERROR] Error en el inicio de sesión: {error_message}")
            except:
                print("[ERROR] Error desconocido en el inicio de sesión")
            
            driver.save_screenshot("error_login.png")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error durante el inicio de sesión: {str(e)}")
        driver.save_screenshot("error_login.png")
        return False

def cerrar_sesion(driver):
    """Cierra la sesión del usuario actual"""
    try:
        # Navegar a la página de perfil donde debería estar el botón de cerrar sesión
        driver.get("http://127.0.0.1:8000/profile/")
        
        # Intentar encontrar y hacer clic en el botón de cerrar sesión
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Cerrar Sesión"))
        ).click()
        
        print("[INFO] Sesión cerrada exitosamente")
        return True
    except Exception as e:
        print(f"[ADVERTENCIA] No se pudo encontrar el botón de cerrar sesión: {str(e)}")
        return False

def main():
    # Configuración de credenciales de prueba
    USUARIO_PRUEBA = generar_usuario_aleatorio()
    CORREO_PRUEBA = generar_correo_aleatorio()
    CONTRASENA_PRUEBA = "Test123!"  # Contraseña de ejemplo que cumple con los requisitos
    
    print(f"\n[INFO] Datos de prueba generados:")
    print(f"Usuario: {USUARIO_PRUEBA}")
    print(f"Correo: {CORREO_PRUEBA}")
    print(f"Contraseña: {CONTRASENA_PRUEBA}")
    
    # Inicializar el navegador
    driver = None
    try:
        print("\n[INFO] Iniciando pruebas de registro e inicio de sesión...")
        driver = configurar_navegador()
        
        # 1. Probar registro de nuevo usuario
        print("\n[PASO 1] Probando registro de nuevo usuario...")
        if registrar_estudiante(driver, USUARIO_PRUEBA, CORREO_PRUEBA, CONTRASENA_PRUEBA, "Test", "Usuario"):
            # 2. Cerrar sesión después del registro exitoso
            cerrar_sesion(driver)
            
            # 3. Probar inicio de sesión con las credenciales recién creadas
            print("\n[PASO 2] Probando inicio de sesión...")
            if iniciar_sesion(driver, USUARIO_PRUEBA, CONTRASENA_PRUEBA):
                # 4. Cerrar sesión después del inicio de sesión exitoso
                cerrar_sesion(driver)
        
        print("\n[INFO] Pruebas completadas")
        
    except Exception as e:
        print(f"\n[ERROR] Error durante la ejecución: {str(e)}")
        if driver:
            driver.save_screenshot("error_ejecucion.png")
    
    finally:
        # Cerrar el navegador
        if driver:
            driver.quit()
            print("\n[FIN] Navegador cerrado")

if __name__ == "__main__":
    main()
