function envi() {
	BASE_DIR=$ENVI_DIR
	[ -z "$BASE_DIR" ] && BASE_DIR=$HOME/.envi

	readonly local action=$1
	readonly local output=$(python3 $BASE_DIR/cli.py $*)
	if [[ "$output" =~ "^##! evaluate" ]]
	then
		source <(echo $output)
	else
		echo "$output"
	fi
}