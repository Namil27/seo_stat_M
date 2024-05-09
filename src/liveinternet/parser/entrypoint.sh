#!/bin/bash

# Сохранение переменных окружения для cron
printenv | grep -v "no_proxy" >> /etc/environment

# Запуск cron
cron -f
