# usage:
# $ cd il1
# $ ../play_il_packet.bash 1

# settings for manual discord / test / in person
ENTER=1
JUSTSLEEP=""
ANSWERPLEASE=""
SAYANSWER=""
PRINTANSWER=1

# settings for auto discord
ENTER=""
JUSTSLEEP=1
ANSWERPLEASE=""
SAYANSWER=1
PRINTANSWER=1

# settings for self playtest
ENTER=1
JUSTSLEEP=""
ANSWERPLEASE=""
SAYANSWER=""
PRINTANSWER=""

#OUTPUTDEVICE=""
# Discord input device should be Loopback,
# which should combine Soundflower (2ch)
# and Built-in Microphone if needed.
# This should be set to the ID of the Multi-Audio Output,
# which splits into Soundflower (2ch) and to Default Output.
OUTPUTDEVICE=41

# Skip questions whose filename contains the string "Hard"
SKIPHARD=""

SAYOD=""
MPLAYEROD=""
if [ $OUTPUTDEVICE ]; then
	SAYOD='-a'$OUTPUTDEVICE
	MPLAYEROD='-ao coreaudio:device_id='$OUTPUTDEVICE
fi


function echosay {
	echo -e "\033[1;33m"$1"\033[0m"
	say $SAYOD $1
	sleep $2
}
function mplay {
	eval "mplayer $MPLAYEROD -msglevel all=0:statusline=9 \"$1\" 2>/dev/null"
}

dir=${1%/}
index=0
let "startat=$2 - 1"
IFS=$'\n'
questions=($(grep -E '^[0-9]+\.' answers/$dir.txt))
# questions=($(grep -E '^(Question|TOSSUP|[0-9]+\.)' answers/$dir.txt))
answers=($(grep -E '^ANSWER' answers/$dir.txt))

# Fonts
BOLD=`tput bold``tput setaf 4`
JUSTBOLD=`tput bold`
BU=`tput bold``tput smul`
BU=`tput smul`
REG=`tput sgr0`
EU=`tput rmul`
CONCEAL=`tput setaf 0``tput setab 0`

echo -en '\nCommands:\n'
echo -e "  • Press ${BOLD}Space${REG} to play/pause a question"
echo -e "  • Press ${BOLD}Ctrl-C${REG} to stop a question early"
echo -e "  • Press ${BOLD}Ctrl-C${REG} again to exit"
echo

for file in $dir/*.mp3; do
	# skip hard
	if [[ $SKIPHARD && $file = *"Hard"* || $index -lt $startat ]]; then
		echo "${BOLD}Skipping ${file##*/}${REG}"
	else

		echo "**${questions[index]}**" | pbcopy
		echosay "${questions[index]}"      1
		answer=`echo ${answers[index]} | sed "s/_\([^_]*\)_/${BU}\1${EU}/g"`
		if [ $PRINTANSWER ]; then
			echo $answer
		else
			echo "<answer hidden> ${CONCEAL}$answer"
			echo "${file##*/}${REG}"
		fi
		echo
		mplay "$file"
		FOO=$?
		echo "${JUSTBOLD}Audio finished.                         ${REG}"
		echo

		echo ${answers[index]} | sed 's/_\([^_]*\)_/__**\1**__/g' | pbcopy

		if [ $ANSWERPLEASE ]; then
			if [ $FOO -ne 1 ]; then
				sleep 4
				echosay "Answer please?"   2
				echosay "Time."            1
			fi
		fi

		if [ $ENTER ]; then
			read -p $'Press enter to continue\n'
		fi

		# replay?

		if [ -z $PRINTANSWER ]; then
			echo $answer

			# TODO: new 2020
			echo
			grep -P "^$(($index+1))\t" clip_descriptions/$dir.tsv 2>/dev/null || echo "(no clip descriptions found)"
		fi

		if [ $SAYANSWER ]; then
			saidanswer=`echo ${answers[index]} | sed "s/_\([^_]*\)_/[[emph 100]]\1/g"`
			say $SAYOD $saidanswer
			sleep 3
		fi
	fi

	echo '————————————————————'
	let index++
done
