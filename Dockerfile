FROM python:3.13

# Establecer el directorio de trabajo en el container
WORKDIR /app

# Copiar el archivo requirements.txt y luego instalar las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY app.py .

# Exponer el puerto que usará el servidor
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
