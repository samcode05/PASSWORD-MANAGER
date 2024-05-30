*GESTOR DE CONTRASEÑAS*
Este proyecto consta de varios archivos que trabajan en conjunto para proporcionar una solución de gestión de contraseñas. Los archivos incluyen:

Un archivo de Python que sirve como el backend de nuestra aplicación. (app.py)
Tres archivos HTML y tres archivos CSS que conforman la interfaz de usuario de nuestra aplicación. (index.html, register.html, index.html, styles.css, register.css, login.css)
Un archivo JavaScript que proporciona funcionalidades adicionales en el frontend.(scripts.js)
Archivos CSV que se utilizan para almacenar datos. (passwords.csv).
Una base de datos alojada en una carpeta llamada ‘instance’.
Un entorno virtual para manejar las dependencias del proyecto. (venv)

*Instalación*
Para poner en marcha el proyecto, sigue estos pasos:

Navega hasta el archivo de Python en una terminal.
Instala todas las bibliotecas requeridas. En este caso, necesitarás Flask. Puedes hacerlo con el comando pip install flask.
Una vez que todas las dependencias estén instaladas, ejecuta el archivo de Python.

*Uso*
Después de ejecutar el archivo de Python, se mostrará una dirección IP en la terminal. Puedes acceder a la aplicación haciendo clic en esta dirección IP con la tecla Control presionada. Esto te permitirá ver cómo funcionan todos los archivos juntos para proporcionar la funcionalidad de gestión de contraseñas.

Una vez que tengas la dirección IP, añade /register al final de la URL. Esto te llevará directamente a la sección de registro, donde podrás crear una cuenta con una contraseña. Después de registrarte, tendrás la opción de iniciar sesión con tu usuario y contraseña.

Una vez que hayas iniciado sesión, serás redirigido a la página principal de nuestro gestor de contraseñas. Aquí, tendrás varias opciones, incluyendo:
Exportar tus contraseñas.
Importar contraseñas.
Agregar nuevas contraseñas.
Eliminar contraseñas existentes.
Editar contraseñas existentes.
Generar contraseñas seguras, con la longitud de caracteres que prefieras.
