#!/bin/sh
set -eu
# Изолированный профиль учебного проекта, без переключения глобального context.
if [ -z "${DOCKER_HOST:-}" ] && [ -S "$HOME/.colima/qa-platform/docker.sock" ]; then
  export DOCKER_HOST="unix://$HOME/.colima/qa-platform/docker.sock"
fi
if docker compose version >/dev/null 2>&1; then
  exec docker compose "$@"
fi
exec docker-compose "$@"
