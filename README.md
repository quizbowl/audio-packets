## Audio packets

### Contents

Currently rehosted without explicit permission. Links to sources (which may not work anymore):

* [Imaginary Landscape No. 1](http://hsquizbowl.org/forums/viewtopic.php?f=21&t=11623&p=219113#p219113)
* [Imaginary Landscape No. 2](http://hsquizbowl.org/forums/viewtopic.php?f=21&t=16234&p=289863#p289863)
* [Imaginary Landscape No. 3](http://hsquizbowl.org/forums/viewtopic.php?f=21&t=18117&p=318076#p318076)
* other sets may be added later

The audio files have been renamed to avoid spoilers.

The original answerline documents are included, and have also been converted to plain text.

### Script

A bash script is included to make playing the packets easier (either by yourself, or in a group).

To play packet 1 from Imaginary Landscape No. 1, for example:

```
cd il1
../play_il_packet.bash 1
```

The script is controlled by the following commands:

* Press <kbd>Space</kbd> to play/pause a question
* Press <kbd>Ctrl-C</kbd> to stop a question early
* Press <kbd>Ctrl-C</kbd> again to exit

The script can be configured by enabling the following flags:

* `ANSWERPLEASE`: waits and says "Answer please?" and "Time" after the question finishes
* `ENTER`: must press enter to continue to the next question
* `SAYANSWER`: says the answer after the question finishes
* `SKIPHARD`: skips questions whose filename contains the string "Hard"

The script has the following requirements:

* `say`: text-to-speech Mac built-in, for speaking the question prompts and answers
* `mplayer`: open-source media player, for playing the audio files
