#!/usr/bin/python
import os, sys, getopt, mutagen
from shutil import copy2

def unkownDir(file, move, output_dir):
    if (not os.path.isdir(os.path.join(output_dir, '###Unknown_Files###'))):
        os.mkdir(os.path.join(output_dir, '###Unknown_Files###'))
        if (verbose):
            print('Created ###Unkown_Files### directory')
    if (move):
        os.rename(file, os.path.join(output_dir, '###Unknown_Files###', os.path.basename(file)))
        if (verbose):
            print('Moved', os.path.basename(file), 'to ###Unkown_Files###')
    else:
        copy2(file, os.path.join(output_dir, '###Unknown_Files###', os.path.basename(file)))
        if (verbose):
            print('Copied', os.path.basename(file), 'to ###Unkown_Files###')
    return True


def unkownArtistDir(file, move, output_dir, album):
    if (not os.path.isdir(os.path.join(output_dir, '###Unkown_Artist###', album))):
        os.makedirs(os.path.join(output_dir, '###Unkown_Artist###', album))
        if (verbose):
            print('Created ###Unkown_Artist### directory')
    if (move):
        os.rename(file, os.path.join(output_dir, '###Unkown_Artist###', album, os.path.basename(file)))
        if (verbose):
            print('Moved', os.path.basename(file), 'to', os.path.join(os.path.basename(
                file), output_dir, '###Unkown_Artist###', album, os.path.basename(file)))
    else:
        copy2(file, os.path.join(os.path.basename(
            file), output_dir, '###Unkown_Artist###', album, os.path.basename(file)))
        if (verbose):
            print('Copied', os.path.basename(file), 'to', os.path.join(os.path.basename(
                file), output_dir, '###Unkown_Artist###', album, os.path.basename(file)))
    return True


def music_move(file, output_dir, album, artist, date, genre, use_date, use_genre):
    if (use_genre and use_date):
        if (not os.path.isdir(os.path.join(output_dir, genre, artist, date, album))):
            os.makedirs(os.path.join(output_dir, genre, artist, date, album))
        os.rename(file, os.path.join(output_dir, genre, artist, date, album, os.path.basename(file)))
        if (verbose):
            print('Moved', os.path.basename(file), 'to', os.path.join(output_dir, genre, artist, date, album, os.path.basename(file)))
    elif (use_genre):
        if (not os.path.isdir(os.path.join(output_dir, genre, artist, album))):
            os.makedirs(os.path.join(output_dir, genre, artist, album))
        os.rename(file, os.path.join(output_dir, genre, artist, album, os.path.basename(file)))
        if (verbose):
            print('Moved', os.path.basename(file), 'to', os.path.join(output_dir, genre, artist, album, os.path.basename(file)))
    elif (use_date):
        if (not os.path.isdir(os.path.join(output_dir, artist, date, album))):
            os.makedirs(os.path.join(output_dir, artist, date, album))
        os.rename(file, os.path.join(output_dir, artist, date, album, os.path.basename(file)))
        if (verbose):
            print('Moved', os.path.basename(file), 'to', os.path.join(output_dir, artist, date, album, os.path.basename(file)))
    else:
        if (not os.path.isdir(os.path.join(output_dir, artist, album))):
            os.makedirs(os.path.join(output_dir, artist, album))
        os.rename(file, os.path.join(output_dir, artist, album, os.path.basename(file)))
        if (verbose):
            print('Moved', os.path.basename(file), 'to', os.path.join(output_dir, artist, album, os.path.basename(file)))
    return True


def music_copy(file, output_dir, album, artist, date, genre, use_date, use_genre):
    if (use_genre and use_date):
        if (not os.path.isdir(os.path.join(output_dir, genre, artist, date, album))):
            os.makedirs(os.path.join(output_dir, genre, artist, date, album))
        copy2(file, os.path.join(output_dir, genre, artist, date, album, os.path.basename(file)))
        if (verbose):
            print('Copied', os.path.basename(file), 'to', os.path.join(output_dir, genre, artist, date, album, os.path.basename(file)))
    elif (use_genre):
        if (not os.path.isdir(os.path.join(output_dir, genre, artist, album))):
            os.makedirs(os.path.join(output_dir, genre, artist, album))
        copy2(file, os.path.join(output_dir, genre, artist, album, os.path.basename(file)))
        if (verbose):
            print('Copied', os.path.basename(file), 'to', os.path.join(output_dir, genre, artist, album, os.path.basename(file)))
    elif (use_date):
        if (not os.path.isdir(os.path.join(output_dir, artist, date, album))):
            os.makedirs(os.path.join(output_dir, artist, date, album))
        copy2(file, os.path.join(output_dir, artist, date, album, os.path.basename(file)))
        if (verbose):
            print('Copied', os.path.basename(file), 'to', os.path.join(output_dir, artist, date, album, os.path.basename(file)))
    else:
        if (not os.path.isdir(os.path.join(output_dir, artist, album))):
            os.makedirs(os.path.join(output_dir, artist, album))
        copy2(file, os.path.join(output_dir, artist, album, os.path.basename(file)))
        if (verbose):
            print('Copied', os.path.basename(file), 'to', os.path.join(output_dir, artist, album, os.path.basename(file)))
    return True


def main(argv):
    global verbose
    input_dir, output_dir = '', ''
    use_genre, use_date, verbose, move, copy_or_move_used = False, False, False, True, False
    try:
        opts, args = getopt.getopt(argv, "cmdhgvi:o:", ["help", "genre", "copy", "move", "date", "verbose", "input=", "output="])
    except getopt.GetoptError:
        print('Invalid syntax. Use -h or --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('\naudiosort -i [unsorted library path] -o [output path]\n\nOptions:\n\t-c or --copy:\n\t\tCopies the files from [input] to [output]\n\t-d or --date:\n\t\tCreate and sort by date\n\t-g or --genre:\n\t\tCreate and sort by genre\n\t-h or --help:\n\t\tShows this message\n\t-i or --input:\n\t\tNeeds a path !\n\t\tIndicates the root directory of the audio library to sort\n\t-m or --move:\n\t\tUsed by default\n\t\tMoves the file from [input] to [output]\n\t-o or --output:\n\t\tNeeds a path !\n\t\tIndicates the root directory of the audio library output\n\t-v or --verbose:\n\t\tShows information for everything the program does')
            sys.exit(0)
        elif opt in ('-v', '--verbose'):
            verbose = True
            print('Using -v or --verbose')
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
        elif opt in ("-i", "--input"):
            input_dir = os.path.abspath(os.path.normpath(arg))
            if (not os.path.isdir(input_dir)):
                print('Error, the input path isn\'t real.')
                sys.exit(2)
        elif opt in ("-o", "--output"):
            output_dir = os.path.abspath(os.path.normpath(arg))
            if (not os.path.isdir(output_dir)):
                create_output_dir = input('The output directory isn\'t real. Do you want to create it? (Y/n)')
                if (create_output_dir == 'Y'):
                    os.makedirs(output_dir)
                else:
                    sys.exit(2)
    if (input_dir == '' or output_dir == ''):
        print('Invalid syntax. You at least need to use -i and -o or --input and --output')
        sys.exit(2)
    if (verbose):
        print('input directory:', input_dir)
        print('output directory:', output_dir)
    for root, dirs, files in os.walk(input_dir):
        for entry in files:
            file, path = entry, root
            os.chdir(path)
            album, artist, date, genre = '', '', '', ''
            f = mutagen.File(file)
            if (f == None):
                continue #TODO Have to take care of other files
            if (verbose):
                print('file:', file)
            if (not 'album' in f):
                unkownDir(entry, move, output_dir)
                continue
            elif ((not 'artist' in f) and (not 'albumartist' in f)):
                album = f['album'][0]
                if (verbose):
                    print('[album]:', album)
                unkownArtistDir(entry, move, output_dir, album)
                continue
            elif (not 'albumartist' in f):
                album = f['album'][0]
                artist = f['artist'][0]
            else:
                album = f['album'][0]
                artist = f['albumartist'][0]
            if (verbose):
                    print('[album]:', album, '\n[artist]:', artist)
            if ('date' in f):
                date = f['date'][0]
            if ('genre' in f):
                genre = f['genre'][0]
            if (verbose):
                    print('[date]:', date, '\n[genre]:', genre)
            if (move):
                music_move(entry, output_dir, album, artist, date, genre, use_date, use_genre)
            else:
                music_copy(entry, output_dir, album, artist, date, genre, use_date, use_genre)        
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
