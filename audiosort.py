#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# audiosort - an audio-library sorter
# Copyright (c) 2019 Docx
#
# Sources on github:
# https://github.com/DocxDocxDocx/audiosort

# MIT License

# Copyright (c) 2019 Docx

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, sys, getopt
from tinytag import TinyTag
from shutil import copy2, rmtree
from shutil import move as mv


def music(file, output_dir, album, artist, date, genre, use_date, use_genre, move):
    if (use_genre and use_date):
        path = os.path.join(output_dir, genre, artist, date, album)
    elif (use_genre):
        path = os.path.join(output_dir, genre, artist, album)
    elif (use_date):
        path = os.path.join(output_dir, artist, date, album)
    else:
        path = os.path.join(output_dir, artist, album)
    os.path.normpath(path)
    if (not os.path.isdir(path)):
        os.makedirs(path)
    file_path = os.path.join(path, os.path.basename(file))
    os.path.normpath(file_path)
    if (os.path.isfile(file_path)):
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
    input_dir, output_dir = None, None
    use_genre, use_date, verbose, move, copy_or_move_used, use_file, use_nuke, auto_yes = False, False, False, True, False, False, False, False
    try:
        opts, args = getopt.getopt(argv, "cmdfnhgyvi:o:", ["yes", "help", "genre", "copy", "move", "date", "verbose", "file", "nuke", "input=", "output="])
    except getopt.GetoptError:
        print('Invalid syntax. Use -h or --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Audiosort is a command line utility to sort your music library\n\nMinimum usage of audiosort:\naudiosort -i [unsorted library path] -o [output path]\n\nOptions:\n\t-c or --copy:\n\t\tCopies the files from [input] to [output]\n\t-d or --date:\n\t\tCreate and sort by date\n\t-f or --file\n\t\tTake care of non-audio files\n\t-g or --genre:\n\t\tCreate and sort by genre\n\t-h or --help:\n\t\tShows this message\n\t-i or --input:\n\t\tNeeds a path !\n\t\tIndicates the root directory of the audio library to sort\n\t-m or --move:\n\t\tUsed by default\n\t\tMoves the file from [input] to [output]\n\t-n or --nuke:\n\t\tRemoves the input directory after sorting it\n\t-o or --output:\n\t\tNeeds a path !\n\t\tIndicates the root directory of the audio library output\n\t-v or --verbose:\n\t\tShows information for everything the program does\n\t-y or --yes:\n\t\tAutomaticly respond yes to any query')
            sys.exit(0)
        elif opt in ('-v', '--verbose'):
            verbose = True
            print('Using -v or --verbose')
        elif opt in ('-y', '--yes'):
            auto_yes = True
            print('Using -y or --yes')
    for opt, arg in opts:
        if opt in ("-g", "--genre"):
            use_genre = True
            if (verbose):
                print('Using -g or --genre')
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
        elif opt in ('-d', '--date'):
            use_date = True
            if (verbose):
                print('Using -d or --date')
        elif opt in ('-f', '--file'):
            use_file = True
            if (verbose):
                print('Using -f or --file')
        elif opt in ('-n', '--nuke'):
            really_nuke = input('Are you sure you want to nuke the input directory? (Y/n)')
            if (auto_yes):
                really_nuke = 'Y'
            if (really_nuke == 'Y'):
                use_nuke = True
                if (verbose):
                    print('Using -n or --nuke')
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
            output_dir = os.path.abspath(os.path.normpath(arg))
            if (not os.path.isdir(output_dir)):
                create_output_dir = input('The output directory isn\'t real. Do you want to create it? (Y/n)')
                if (auto_yes):
                    create_output_dir = 'Y'
                if (create_output_dir == 'Y'):
                    os.makedirs(output_dir)
                else:
                    sys.exit(2)
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
            album, artist, date, genre = '###UNKNOWN_ALBUM###', '###UNKNOWN_ARTIST###', '###UNKNOWN_DATE###', '###UNKNOWN_GENRE###'
            if (verbose):
                print('--------------------')
            if (not TinyTag.is_supported(file)):
                if (use_file):
                    dir_path = os.path.join(output_dir, '###OTHER_FILES###')
                    file_path = os.path.join(dir_path, file)
                    os.path.normpath(dir_path)
                    os.path.normpath(file_path)
                    if (not os.path.isdir(dir_path)):
                        os.makedirs(dir_path)
                    if (not os.path.isfile(file_path)):
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
                album = f.album
            if (not f.albumartist == None):
                album = f.albumartist
            elif (not f.artist == None):
                artist = f.artist
            if (verbose):
                    print('[album]:', album, '\n[artist]:', artist)
            if (not f.year == None):
                date = f.year
            if (not f.genre == None):
                genre = f.genre
            if (verbose):
                    print('[date]:', date, '\n[genre]:', genre)
            if ((not music(entry, output_dir, album, artist, date, genre, use_date, use_genre, move)) and verbose):
                print('File skipped because it\'s already in the library')
            if (verbose):
                print('--------------------\n')
    if (use_nuke):
        rmtree(input_dir)
        if (verbose):
            print('Nuked the input directory')
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
