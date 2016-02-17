from PyPDF2 import PdfFileMerger, PdfFileReader
import os


def ask(question, cursor='>> ', default_choice=None):
    '''This is a shortcut function to ask questions and receive a string answer
    back. The `question` is a string which is printed out in the console.
    `cursor` is the delimiter used to prompt the user to enter an answer. If
    provided, `default_choice` is returned if no input is provided,'''
    actual_question = question

    if default_choice:
        actual_question = '{} [Default: {}]'.format(question, default_choice)

    print(actual_question)
    answer = input(cursor)

    if answer:
        return answer
    elif default_choice:
        return default_choice
    else:
        return ''


def ask_for_directory():
    '''Prompt the user which directory to work on. Defaults to the present
    working directory.'''
    return ask('What directory contains your PDFs? Please enter the absolute '
               'path.', default_choice=os.getcwd())


def is_valid_directory(directory):
    '''Verify if `directory` is indeed a directory.'''
    return directory and os.path.isdir(directory)


def list_files(directory):
    '''Returns a list of files within `directory` that end with the
    `extension`.'''
    files = [file_name for file_name in os.listdir(directory)
             if file_name.endswith('pdf')]
    files.sort()
    return files


def should_include_file(_file):
    '''Identifies whether or not the user wants to include `_file`.'''
    response = None
    while not response:
        response = ask('Include {}? [y/n]'.format(_file)).lower()

        if response != 'y' and response != 'n':
            response = None

    return response == 'y'


def ask_for_selection(directory, files):
    '''Lists the `directory` files and returns a list of the files that the user
    wants to include.'''
    return [os.path.join(directory, _file) for _file in files
            if should_include_file(_file)]



def ask_for_new_file_name():
    '''Asks for the file name of the new merged file.'''
    return ask('What would you like to name the combined file?')


def build_file_name(file_name):
    '''Returns the file name entered.'''
    return '{}.pdf'.format(file_name)


def merge(file_names, new_file_name):
    '''Merges the list of `file_names` into one file called `new_file_name`.'''
    merger = PdfFileMerger()

    for file_name in file_names:
        merger.append(PdfFileReader(file_name, 'rb'))

    merger.write(new_file_name)


def ask_for_destination(file_name, default=os.getcwd()):
    '''Asks the user where they would like to save the `file_name`. It defaults
    to save `file_name` to the directory `default`.'''
    destination = ask('Where would you like to save {}?'.format(file_name), default)

    if not is_valid_directory(destination):
        destination = default

    return os.path.join(destination, file_name)


def ask_where_to_work():
    '''Asks the user what directory to look for files. It expects an absolute
    path.'''
    directory = None

    while not is_valid_directory(directory):
        directory = ask_for_directory()

    return directory


def go_for_it(workspace, files, extension):
    '''This is the main logic to merge the files.'''
    selection = ask_for_selection(workspace, files)
    new_file_name = build_file_name(ask_for_new_file_name(), extension)
    destination = ask_for_destination(new_file_name, workspace)
    merge(selection, destination)
    print('Created `{}`'.format(destination))


def main():
    '''Executes the program. Try it out. :D '''
    directory = ask_where_to_work()
    extension = ask_for_file_type()
    files = list_files(directory)

    if len(files) > 0:
        go_for_it(directory, files, extension)
    else:
        print('No files were found in `{}`'.format(directory))

if __name__ == '__main__':
    main()
