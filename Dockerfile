FROM php:8.4-fpm as base
RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y libpq-dev && \
    docker-php-ext-install pdo_pgsql opcache && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

COPY --from=compose:latest /usr/bin/composer /usr/bin/composer
WORKDIR /var/www

COPY composer.lock composer.json ./
RUN composer install --no-interaction --prefer-dist --no-scripts

COPY . .
RUN chown -R www-data:www-data storage bootstrap/cache

FROM base as testing
ENV APP_ENV=testing
CMD ["php", "artisan", "test"]

FROM base as dev
ENV APP_ENV=local
ENV APP_DEBUG=true

FROM base as prod
ENV APP_ENV=production
ENV APP_DEBUG=false
RUN composer install --no-interaction --prefer-dist --optimize-autoloader --no-dev
