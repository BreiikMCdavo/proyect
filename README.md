SISTEMA WEB ASISTCONTROL "Un sistema de control de Asistencias" 
![Image](https://github.com/user-attachments/assets/29636c85-aaba-494f-ae38-b4c1381bc6a2)
![Image](https://github.com/user-attachments/assets/9765727b-5a8d-4dd9-9a60-644319e30783)
![Image](https://github.com/user-attachments/assets/97bb867b-0f66-40cf-ba25-dee767942a23)
![Image](https://github.com/user-attachments/assets/3228bbf8-fd80-4cdf-a6cf-0ae05d51b25f)
![Image](https://github.com/user-attachments/assets/cf4d7503-6725-4676-99d1-077fab729b8d)
![Image](https://github.com/user-attachments/assets/b7d2aa8b-593b-4178-b31a-672185c9203d)
# 1. Crear y activar entorno virtual (recomendado)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

# 2. Instalar las dependencias desde requirements.txt
pip install -r requirements.txt

# 3. (Opcional) Exportar las variables de entorno para Flask (Linux/Mac)
export FLASK_APP=app.py
export FLASK_ENV=development

# En Windows CMD
set FLASK_APP=app.py
set FLASK_ENV=development

# 4. Ejecutar la aplicación Flask en modo desarrollo
flask run
