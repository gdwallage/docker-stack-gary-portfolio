#!/bin/bash
# ==============================================================================
# Gary Wallage WordPress Multisite Dynamic Swarm Cron Runner
# ==============================================================================

# Prevent overlapping runs: if a previous invocation is still mid-flight
# (e.g. a slow GMS sync scan) when the next 5-minute tick fires, skip this
# tick entirely rather than stacking another full pass on top of it. Without
# this, invocations pile up indefinitely under load and each one competes
# for the same DB/CPU, making every one of them slower still.
LOCKFILE="/tmp/gw-run-cron.lock"
exec 200>"$LOCKFILE"
flock -n 200 || { echo "[$(date)] Skipping run: previous invocation still in progress." >&2; exit 0; }

SITES=(
    "https://garywallage.uk"
    "https://wedding.garywallage.uk"
    "https://family.garywallage.uk"
    "https://fashion.garywallage.uk"
    "https://cosplay.garywallage.uk"
    "https://glamour.garywallage.uk"
    "https://boudoir.garywallage.uk"
)

# Find active WordPress Swarm container
CID=$(docker ps --filter "name=gary-portfolio_wordpress" --filter "status=running" --format "{{.ID}}" | head -n 1)

if [ -z "$CID" ]; then
    echo "[$(date)] ERROR: No running gary-portfolio_wordpress container found in Swarm." >&2
    exit 1
fi

# Run WP-Cron for each subsite
for site in "${SITES[@]}"; do
    docker exec -u sickchill "$CID" wp cron event run --due-now --url="$site" --quiet > /dev/null 2>&1
done
