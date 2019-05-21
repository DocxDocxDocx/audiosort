# Audiosort
A small audio library sorter command line utility

Using TinyTag for metadata reading. Check it out! https://github.com/devsnd/tinytag

### Usage:
```
audiosort -i [unsorted library path] -o [output path]

Options:
	-c or --copy:
		Copies the files from [input] to [output]
	-d or --date:
		Create and sort by date
	-f or --file
		Take care of non-audio files
	-g or --genre:
		Create and sort by genre
	-h or --help:
		Shows this message
	-i or --input:
		Needs a path !
		Indicates the root directory of the audio library to sort
	-m or --move:
		Used by default
		Moves the file from [input] to [output]
	-n or --nuke:
		Removes the input directory after sorting it
	-o or --output:
		Needs a path !
		Indicates the root directory of the audio library output
	-v or --verbose:
		Shows information for everything the program does
```
