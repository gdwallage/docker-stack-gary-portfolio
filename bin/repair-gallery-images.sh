#!/bin/bash
# ==============================================================================
# Gary Wallage WordPress Multisite Gallery Master Sync — Hourly Self-Repair
#
# Re-runs GMS_Sync_Engine::upsert_attachment() for any GMS-synced attachment
# whose full-size file is missing or whose _wp_attachment_metadata has no
# generated sizes (the failure signature of the pre-4b652bf output-format
# filter bug). Safe to run repeatedly: it only touches attachments that are
# still broken, and re-derives them from the untouched source master files.
# ==============================================================================

# Prevent overlapping runs (same reasoning as run-cron.sh's lock): a full
# repair pass across all sites can run long under load, and an hourly tick
# firing on top of a still-running one would double CPU/DB load instead of
# finishing sooner.
LOCKFILE="/tmp/gw-repair-gallery.lock"
exec 200>"$LOCKFILE"
flock -n 200 || { echo "[$(date)] Skipping run: previous repair pass still in progress." >&2; exit 0; }

CID=$(docker ps --filter "name=gary-portfolio_wordpress" --filter "status=running" --format "{{.ID}}" | head -n 1)

if [ -z "$CID" ]; then
    echo "[$(date)] ERROR: No running gary-portfolio_wordpress container found in Swarm." >&2
    exit 1
fi

docker exec -u sickchill "$CID" php /var/www/html/repair-thumbnails.php
