# Audiosort
A small audio library sorter command line utility under MIT license.

Using TinyTag for metadata reading. Check it out! https://github.com/devsnd/tinytag

### Usage:
```
Minimum usage of audiosort:
audiosort -i [unsorted library path] -o [output path]

If one of the tags contains an illegal character for your OS it will be replaced by a "#"

Patterns can be used in the output path and filename like so:
%{tag}

Usable tags:
    album
    albumartist, artist, realartist (use artist rather than realartist)
    audio_offset
    bitrate
    comment
    composer
    disc
    disc_total
    duration
    filesize
    genre
    samplerate
    title
    track
    track_total
    year

Options:
	-c or --copy:
		Copies the files from [input] to [output]
	-f or --file
		Needs a path !
        Take care of unsuported files
	-h or --help:
		Shows this message
	-i or --input:
		Needs a path !
		Indicates the root directory of the audio library to sort
    --legal:
        Shows the license of the program
	-m or --move:
		Used by default
		Moves the file from [input] to [output]
	-n or --filename:
        Needs a filename pattern (with tags)
        Renames the sorted files to the pattern
    --nuke:
		Removes the input directory after sorting it
	-t or --overwrite or --thwomp:
		If a file exist already then it's overwritten
	-o or --output:
		Needs a path !
		Indicates the directory of the audio library output
	-v or --verbose:
		Shows information for everything the program does
	-y or --yes:
		Automatically respond yes to any query
```