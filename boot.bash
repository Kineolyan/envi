function envi() {
	BASE_DIR=$ENVI_DIR
	[ -z "$BASE_DIR" ] && BASE_DIR=$HOME/.envi

	readonly local action=$1
	if [ "$action" = "shell" ]
	then
		source <(python3 "$BASE_DIR/cli.py" $*)
	else
		python3 $BASE_DIR/cli.py $*
	fi
}