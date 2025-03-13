# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación en el contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que el servidor escuchará
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "src/main/python/main.py"]

# docker build -t server .
# docker run -d -p 8080:8080 server