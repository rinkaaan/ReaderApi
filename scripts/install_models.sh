WORKPLACE="$HOME/workplace/Reader"

(
  cd "$WORKPLACE/ReaderModels"
  pip install .
  rm -rf build
)
