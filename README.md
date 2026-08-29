# Gary Portfolio — Docker Infrastructure Stack

Production Docker stack and container definitions for Gary Wallage Photography WordPress Multisite network.

## Architecture
- **Web (`nginx`)**: High-performance reverse proxy for static assets and PHP-FPM fastcgi passing.
- **App (`wordpress`)**: Custom hardened PHP-FPM Alpine container with GD, WebP, AVIF, Imagick, Redis, and SVGO CLI tools.
- **Database (`mariadb`)**: MariaDB 11.4 with InnoDB buffer pool optimization and slow query logging.
- **Cache**: Redis object cache layer.
- **Media Storage**: Read-only bind mount from `/srv/media/copyright` to `/var/www/html/wp-content/uploads/galleries`.

## Stack Management
```bash
# Build custom WordPress container
docker build -t gary-portfolio-local:latest .

# Deploy / restart stack
docker compose up -d
```
