# Imagen base de Nginx
FROM nginx:alpine

# Copiar archivos del frontend al directorio de Nginx
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY README.md /usr/share/nginx/html/

# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer el puerto 80
EXPOSE 80

# Nginx se ejecuta automáticamente como proceso principal
CMD ["nginx", "-g", "daemon off;"]
