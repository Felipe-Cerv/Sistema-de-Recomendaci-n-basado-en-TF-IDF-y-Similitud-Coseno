# Solución Rápida - Docker Compose Error en Linux

Si obtienes este error:
```
urllib3.exceptions.URLSchemeUnknown: Not supported URL scheme http+docker
```

## Solución

Usa `docker compose` (sin guión) en lugar de `docker-compose`:

```bash
# En lugar de
docker-compose up -d

# Usa
docker compose up -d
```

## Si no funciona, instala Docker Compose V2

```bash
# Para Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Verificar instalación
docker compose version
```

## Comandos actualizados

```bash
# Iniciar
docker compose up -d

# Ver logs
docker compose logs -f

# Detener
docker compose down

# Reconstruir
docker compose build --no-cache
docker compose up -d
```

## Verificar versión de Docker

```bash
docker --version
docker compose version
```

Deberías ver algo como: `Docker Compose version v2.x.x`
