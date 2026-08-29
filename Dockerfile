# ==========================================
# STAGE 1: THE BUILD ENGINE (Compilers & Tools)
# ==========================================
FROM wordpress:fpm-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    autoconf \
    build-base \
    linux-headers \
    freetype-dev \
    libjpeg-turbo-dev \
    libpng-dev \
    libwebp-dev \
    libavif-dev \
    imagemagick-dev \
    libzip-dev \
    git \
    unzip

# Configure and compile PHP extensions
RUN docker-php-ext-configure gd \
    --with-freetype \
    --with-jpeg \
    --with-webp \
    --with-avif \
    && docker-php-ext-install -j$(nproc) gd

RUN pecl install redis && docker-php-ext-enable redis

# ==========================================
# STAGE 2: THE SECURE RUNTIME (Production)
# ==========================================
FROM wordpress:fpm-alpine

# Install ONLY runtime utilities needed by image optimization plugins
RUN apk add --no-cache \
    freetype \
    libjpeg-turbo \
    libpng \
    libwebp \
    libavif \
    imagemagick \
    libzip \
    libgomp \
    jpegoptim \
    libjpeg-turbo-utils \
    optipng \
    pngquant \
    gifsicle \
    nodejs \
    mariadb-client

# Copy globally installed SVGO and compiled extensions from the builder stage
COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/

# Install SVGO cleanly using a temporary npm cache, then strip npm entirely
RUN apk add --no-cache npm && npm install -g svgo && apk del npm

# Create the explicit host-matching Group and User accounts
RUN addgroup -g 2000 media && \
    adduser -u 2000 -D -S -G media sickchill

# Inject optimized PHP OPcache settings
RUN { \
        echo 'opcache.memory_consumption=256'; \
        echo 'opcache.interned_strings_buffer=16'; \
        echo 'opcache.max_accelerated_files=10000'; \
        echo 'opcache.revalidate_freq=60'; \
        echo 'opcache.fast_shutdown=1'; \
        echo 'opcache.enable_cli=1'; \
    } > /usr/local/etc/php/conf.d/opcache-custom.ini

# Inject performance pool configuration aligned to UID/GID 2000
RUN { \
        echo '[www]'; \
        echo 'user = sickchill'; \
        echo 'group = media'; \
        echo 'pm = dynamic'; \
        echo 'pm.max_children = 24'; \
        echo 'pm.start_servers = 6'; \
        echo 'pm.min_spare_servers = 4'; \
        echo 'pm.max_spare_servers = 12'; \
        echo 'pm.max_requests = 1000'; \
    } > /usr/local/etc/php-fpm.d/zz-docker-performance.conf

# Clean up webroot and assign absolute ownership to the custom user space
WORKDIR /var/www/html
RUN chown -R sickchill:media /var/www/html

# Enforce secure system execution context matching host boundaries
USER sickchill
