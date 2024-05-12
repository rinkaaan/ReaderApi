WORKPLACE="$HOME/workplace/Reader"
WORKSPACE="$WORKPLACE/ReaderApi"

(
  cd "$WORKSPACE/api"
  flask spec --output openapi.yaml > /dev/null
)
