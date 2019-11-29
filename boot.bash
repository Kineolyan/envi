function envi() {
	BASE_DIR=$ENVI_DIR
	[ -z "$BASE_DIR" ] && BASE_DIR=$HOME/.envi

	source <(python3 "$BASE_DIR/entrypoint.py" $*)
}