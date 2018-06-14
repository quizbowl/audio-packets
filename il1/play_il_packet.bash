function echosay {
	echo -e "\033[1;33m"$1"\033[0m"
	say $1
	sleep $2
}
function mplay {
	mplayer -msglevel all=0:statusline=9 $1
}

dir=$1
index=0
IFS=$'\n'
questions=($(grep -E '^[0-9]+\.' answers/$dir.txt))
# questions=($(grep -E '^(Question|TOSSUP|[0-9]+\.)' answers/$dir.txt))
answers=($(grep -E '^ANSWER' answers/$dir.txt))

# Fonts
BOLD=`tput bold``tput setaf 4`
REG=`tput sgr0`

echo -en '\nCommands:\n'
echo -e "  • Press ${BOLD}Space${REG} to play/pause a question"
echo -e "  • Press ${BOLD}Ctrl-C${REG} to stop a question early"
echo -e "  • Press ${BOLD}Ctrl-C${REG} again to exit"
echo

for file in $dir/*.mp3; do
	echosay "${questions[index]}"  1
	echo ${answers[index]}
	echo
	mplay $file
	FOO=$?
	echo "Audio finished.       "
	if [ $FOO -ne 1 ]; then
		sleep 4
		# echosay "Answer please?"   2
		# echosay "Time."            1
	fi
	# echosay ${answers[index]}      3
	echo ${answers[index]}
	echo '————————————————————'
	let index++
done
