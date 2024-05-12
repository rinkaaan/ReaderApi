source ~/startup.sh
WORKPLACE="$HOME/workplace/Reader"

WORKSPACE="$WORKPLACE/ReaderApi"
(
  cd "$WORKSPACE"
  rsync-project Reader
  ssh root@hetzner "pm2 restart api-media"
)
