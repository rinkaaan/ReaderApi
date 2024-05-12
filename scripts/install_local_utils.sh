WORKPLACE="$HOME/workplace/Reader"

(
  cd "$WORKPLACE/PythonUtils"
  pip install .
  rm -rf build
)
