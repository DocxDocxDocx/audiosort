#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, getopt
from tinytag import TinyTag
from string import Template
from shutil import copy2, rmtree
from shutil import move as mv


class TemplateP(Template):
        delimiter = '%'


def music(file, output_dir, filetags, move, use_over, filename):
    path = TemplateP(output_dir).safe_substitute(filetags)
    os.path.normpath(path)
    os.path.abspath(path)
    if (not os.path.isdir(path)):
        os.makedirs(path)
    if (not filename == os.path.basename(file)):
        for e in ['.mp3','.oga','.ogg','.opus','.wav','.flac','.wma','.m4b','.m4a','.mp4']:
            if os.path.basename(file).lower().endswith(e):
                ext = e
                break
        filename = TemplateP(filename).safe_substitute(filetags) + ext
    file_path = os.path.join(path, filename)
    os.path.normpath(file_path)
    if (os.path.isfile(file_path) and (not use_over)):
        return False
    if (move):
        mv(file, file_path)
        m_or_c = 'Moved'
    else:
        copy2(file, file_path)
        m_or_c = 'Copied'
    if (verbose):
        print(m_or_c, os.path.basename(file), 'to', file_path)
    return True


def main(argv):
    global verbose
    if sys.platform.startswith('freebsd') or sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        illegal_chars = ['.','/']
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        illegal_chars = ['<','>',':','\"','/','\\','|','?','*','.']
    input_dir, output_dir, filename = None, None, None
    verbose, move, copy_or_move_used, use_file, use_nuke, auto_yes, use_over, use_filename = False, True, False, False, False, False, False, False
    try:
        opts, args = getopt.getopt(argv, "cmthyvf:n:i:o:", ["yes", "help", "legal", "copy", "move", "verbose", "file=", "nuke", "thwomp", "overwrite", "filename=", "input=", "output="])
    except getopt.GetoptError:
        print('Invalid syntax. Use -h or --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Audiosort is a command line utility to sort your music library\n\nMinimum usage of audiosort:\naudiosort -i [unsorted library path] -o [output path]\n\nIf one of the tags contains an illegal character for your OS it will be replaced by a "#"\n\nPatterns can be used in the output path and filename like so:\n%{tag}\n\nUsable tags:\n\talbum\n\talbumartist, artist, realartist (use artist rather than realartist)\n\taudio_offset\n\tbitrate\n\tcomment\n\tcomposer\n\tdisc\n\tdisc_total\n\tduration\n\tfilesize\n\tgenre\n\tsamplerate\n\ttitle\n\ttrack\n\ttrack_total\n\tyear\n\nOptions:\n\t-c or --copy:\n\t\tCopies the files from [input] to [output]\n\t-f or --file\n\t\tNeeds a path !\n\t\tTake care of unsuported files\n\t-h or --help:\n\t\tShows this message\n\t-i or --input:\n\t\tNeeds a path !\n\t\tIndicates the root directory of the audio library to sort\n\t--legal:\n\t\tShows the license of the program\n\t-m or --move:\n\t\tUsed by default\n\t\tMoves the file from [input] to [output]\n\t-n or --filename:\n\t\tNeeds a filename pattern (with tags)\n\t\tRenames the sorted files to the pattern\n\t--nuke:\n\t\tRemoves the input directory after sorting it\n\t-t or --overwrite or --thwomp:\n\t\tIf a file exist already then it\'s overwritten\n\t-o or --output:\n\t\tNeeds a path !\n\t\tIndicates the directory of the audio library output\n\t-v or --verbose:\n\t\tShows information for everything the program does\n\t-y or --yes:\n\t\tAutomatically respond yes to any query')
            sys.exit(0)
        elif opt in ('-v', '--verbose'):
            verbose = True
            print('Using -v or --verbose')
        elif (opt == '--legal'):
            print(legal)
            sys.exit(0)
        elif opt in ('-y', '--yes'):
            auto_yes = True
            print('Using -y or --yes')
    for opt, arg in opts:
        if opt in ("-t", "--overwrite", "thwomp"):
            really_over = input('Are you sure you want to overwrite files ?(Y/n)')
            if (auto_yes):
                really_over = 'Y'
            if (really_over == 'Y'):
                use_over = True
                if (verbose):
                    print('Using -t or --overwrite or --thwomp')
            else:
                if (verbose):
                    print('Not Using -t or --overwrite or --thwomp then')
        elif opt in ('-c', '--copy'):
            if (not copy_or_move_used):
                move = False
                copy_or_move_used = True
                if (verbose):
                    print('Using -c or --copy')
            else:
                print('Both -c and -m or --copy and --move are used. Using --move by default')
                move = True
        elif opt in ('-m', '--move'):
            if (not copy_or_move_used):
                move = True
                copy_or_move_used = True
                if (verbose):
                    print('Using -m or --move')
            else:
                print('Both -c and -m or --copy and --move are used. Using --move by default')
                move = True
        elif opt in ('-f', '--file'):
            use_file = True
            other_files_path = os.path.abspath(arg)
            if (not os.path.isdir(other_files_path)):
                os.makedirs(other_files_path)
            if (verbose):
                print('Using -f or --file')
        elif opt in ('-n', '--filename'):
            filename = arg
            use_filename = True
            if (verbose):
                print('Using -n or --filename')
        elif (opt == '--nuke'):
            really_nuke = input('Are you sure you want to nuke the input directory? (Y/n)')
            if (auto_yes):
                really_nuke = 'Y'
            if (really_nuke == 'Y'):
                use_nuke = True
                if (verbose):
                    print('Using --nuke')
            else:
                use_nuke = False
                if (verbose):
                    print('Not using -n or --nuke then')
        elif opt in ("-i", "--input"):
            input_dir = os.path.abspath(os.path.normpath(arg))
            if (os.path.isfile(input_dir)):
                print('Error, the input path is pointing to a file')
                sys.exit(2)
            elif (not os.path.isdir(input_dir)):
                print('Error, the input path isn\'t real.')
                sys.exit(2)
        elif opt in ("-o", "--output"):
            output_dir = os.path.abspath(arg)
    if (input_dir == None or output_dir == None):
        print('Invalid syntax. You at least need to use -i and -o or --input and --output')
        sys.exit(2)
    if (verbose):
        print('input directory:', input_dir)
        print('output directory:', output_dir)
    for root, dirs, files in os.walk(input_dir):
        for entry in files:
            file, path = entry, root
            os.chdir(path)
            filetags = {'album':'###UNKNOWN_ALBUM##', 'albumartist': '###UNKNOWN_ALBUM_ARTIST###','realartist':'###UNKNOWN_ARTIST###', 'artist':'###UNKNOWN_ARTIST###' , 'audio_offset':'###UNKNOWN_AUDIO_OFFSET###' , 'bitrate':'###UNKNOWN_BITRATE###' , 'comment':'###UNKNOWN_COMMENT###' , 'composer':'###UNKNOWN_COMPOSER###' , 'disc':'###UNKNOWN_DISC###' , 'disc_total':'###UNKNOWN_DISC_TOTAL###' , 'duration':'###UNKNOWN_DURATION###' , 'filesize':'###UNKNOWN_FILESIZE###' , 'genre':'###UNKNOWN_GENRE###' , 'samplerate':'###UNKNOWN_SAMPLERATE###' , 'title':'###UNKNOWN_TITLE###' , 'track':'###UNKNOWN_TRACK###' , 'track_total':'###UNKNOWN_TRACK_TOTAL###', 'year':'###UNKNOWN_YEAR###'}
            if (verbose):
                print('--------------------')
            if (not TinyTag.is_supported(file)):
                if (use_file):
                    file_path = os.path.join(other_files_path, file)
                    os.path.normpath(file_path)
                    if (not os.path.isfile(file_path) or use_over):
                        m_or_c = ''
                        if (move):
                            mv(os.path.join(root, file), file_path)
                            m_or_c = 'Moved'
                        else:
                            copy2(os.path.join(root, file), file_path)
                            m_or_c = 'Copied'
                        if (verbose):
                            print(m_or_c, os.path.basename(file), 'to', file_path)
                    else:
                        print('File skipped because it\'s already in the library')
                else:
                    if (verbose):
                        print('File skipped because it\'s not an audio file')
                if (verbose):
                    print('--------------------\n')
                continue
            f = TinyTag.get(file)
            if (verbose):
                print('file:', file)
            if (not f.album == None):
                filetags['album'] = f.album
            if (not f.albumartist == None):
                filetags['artist'] = f.albumartist
                filetags['albumartist'] = f.albumartist
            if (not f.artist == None):
                if (f.albumartist == None):
                    filetags['artist'] = f.artist
                filetags['realartist'] = f.artist
            if (not f.year == None):
                filetags['year'] = str(f.year)
            if (not f.genre == None):
                filetags['genre'] = f.genre
            if (not f.audio_offset == None):
                filetags['audio_offset'] = str(f.audio_offset)
            if (not f.bitrate == None):
                filetags['bitrate'] = str(f.bitrate)
            if (not f.comment == None):
                filetags['comment'] = f.comment
            if (not f.composer == None):
                filetags['composer'] = f.composer
            if (not f.disc == None):
                filetags['disc'] = f.disc
            if (not f.disc_total == None):
                filetags['disc_total'] = str(f.disc_total)
            if (not f.duration == None):
                filetags['duration'] = str(f.duration)
            if (not f.filesize == None):
                filetags['filesize'] = str(f.filesize)
            if (not f.samplerate == None):
                filetags['samplerate'] = str(f.samplerate)
            if (not f.title == None):
                filetags['title'] = f.title
            if (not f.track == None):
                filetags['track'] = str(f.track)
            if (not f.track_total == None):
                filetags['track_total'] = str(f.track_total)
            if (verbose):
                for x, y in filetags.items():
                    print('[{0}]:{1}'.format(x,y))
            for c in illegal_chars:
                for i in filetags.values():
                    i.replace(c, '#')
            if (not use_filename):
                filename = file
            if ((not music(entry, output_dir, filetags, move, use_over, filename)) and verbose):
                print('File skipped because it\'s already in the library')
            if (verbose):
                print('--------------------\n')
    if (use_nuke):
        rmtree(input_dir)
        if (verbose):
            print('Nuked the input directory')
    sys.exit(0)

legal = """audiosort - an audio-library sorter
Copyright (c) 2019 Docx

Sources on github:
https://github.com/DocxDocxDocx/audiosort

MIT License
Copyright (c) 2019 Docx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

if __name__ == "__main__":
    main(sys.argv[1:])
