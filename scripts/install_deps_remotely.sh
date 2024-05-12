source ~/startup.sh
WORKPLACE="$HOME/workplace/Reader"

WORKSPACE="$WORKPLACE/ReaderApi"
(
  cd "$WORKSPACE"
  rsync-project Reader
  ssh root@hetzner "source ~/startup.sh && cd ~/workplace/Reader/ReaderApi && py-install"
)
