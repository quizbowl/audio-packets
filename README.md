## Audio packets

### Contents

Currently rehosted without explicit permission. Links to forum threads and sources (which may not work anymore):

* [Imaginary Landscape No. 1](http://hsquizbowl.org/forums/viewtopic.php?f=21&t=11623&p=219113#p219113) (2011)
  * Source:
[1](https://app.box.com/s/cjz4h8mtmpexg54hwp47)
[2](https://app.box.com/s/rkog5lzgv5z08h3rz9edjtslame5sna5)
[3](https://app.box.com/s/dvim5i3jw47pca15nmh6)
[4](https://app.box.com/s/qgvoru61whvqn8owjn04)
[5](https://app.box.com/s/4w8styo3zcegiipadwwn)
[6](https://app.box.com/s/uxxq16t3nayudhlcv8p1)
[7](https://app.box.com/s/p0p6fjvhrxxq0xcobate)
[8](https://app.box.com/s/lus2brcnvbszm6gi5b27)
* [Imaginary Landscape No. 2](http://hsquizbowl.org/forums/viewtopic.php?f=21&t=16234&p=289863#p289863) (2014)
  * Source:
[1](https://app.box.com/s/9cjrh6f96um752scc4vk)
[2](https://app.box.com/s/apg3kusvq0iiqfvcwfj9)
[3](https://app.box.com/s/l66tytwjmejq7pzi1ukj)
[4](https://app.box.com/s/2w2ztx8ze9x6jvu5u67f)
[5](https://app.box.com/s/hcy6za2tiooehv5ymdm2)
[6](https://app.box.com/s/souowe39meed1nzn2evs)
[7](https://app.box.com/s/41werd8fdlvbqrgxzyn0)
[8](https://app.box.com/s/wuhmam1jr4ayu8mkjq1g)
* [Imaginary Landscape No. 3](http://hsquizbowl.org/forums/viewtopic.php?f=21&t=18117&p=318076#p318076) (2016)
  * Source: [All packets](https://app.box.com/s/2bjv3rmjdabi4a5whdh3g4zwmzlmvxub)
* [Imaginary Landscape No. 4](http://hsquizbowl.org/forums/viewtopic.php?f=8&t=20394) (2018)
* [Imaginary Landscape No. 5](https://hsquizbowl.org/forums/viewtopic.php?t=21583) (2019)
* [Guerilla Imaginary Landscape](http://hsquizbowl.org/forums/viewtopic.php?f=8&t=21409) (2018)
* [SOUNDTRACK](http://hsquizbowl.org/forums/viewtopic.php?f=19&t=20359) (2018)
  * Source: [All packets](http://trash.quizbowlpackets.com/2176/)
* other sets may be added later

The audio files have been renamed to avoid spoilers.

The original answerline documents are included, and have also been converted to plain text.

### Script

A bash script is included to make playing the packets easier (either by yourself, or in a group).
It merely reads each question prompt out loud before playing the corresponding audio file, and goes through a single directory in order.

This section assumes that you already know how to use a command line interface to change the directory and run a simple program.
It was written for my own personal use (on a Mac), so it may not work for you out of the box.

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

---

## How to download

The options are listed with the most recommended one first.

1. Use any git client (either command line or desktop) to clone the whole repository. This will keep all the packets in one place. Any updates can easily be downloaded with a simple `git pull`.
2. Click the green `Clone or download` button above, then `Download ZIP` to download the whole repository.
3. Using GitHub’s online interface, navigate to an audio file and click either `View Raw` or `Download`. You may need to use a browser like Firefox instead of Google Chrome. This is because GitHub intentionally serves all raw files as `plain/text`, regardless of the actual type. Firefox plays these audio files because it tries to detect the type of any file, instead of trusting what GitHub’s server says.

---

## How to play audio over Discord

### Gist of these instructions

Your computer can have multiple “audio devices,” such as a microphone, a speaker, or a virtual audio device that you might need to create anew.

* Change the _output_ audio device in your _media player_ from “speaker” to the virtual device.
  * If you also want to hear your media player’s audio through your speakers/headphones, you will need to create a “multi-output device” that outputs simultaneously to _both_ “speaker” (or default output) _and_ the virtual device. Then change the output audio device in your media player to this new multi-output device.
* Change the _input_ audio device in your _Discord voice settings_ from “microphone” to the virtual device.
  * If you also want to talk into your microphone while playing music, you will need to combine “microphone” and the virtual device by doing something more complicated.

Search `how to play music through mic` on Google for more information on this topic.

### Mac

Install [Soundflower](https://rogueamoeba.com/freebies/soundflower/) (a Mac extension for interapplication audio routing) and use `Soundflower (2ch)` as the virtual device. Change the media player output to `Soundflower (2ch)` and the Discord input to `Soundflower (2ch)`.

### Windows

Install something like [Cable](https://www.vb-audio.com/Cable/) to use virtual devices.

### Discord settings

Your Discord voice settings should look similar to the following image. Disable echo, silence, and noise detection (as these features are intended for conversational speech). Change the bitrate of the Discord voice channel to 96 kbps.

<img src="discord-settings.png" width="614" />
