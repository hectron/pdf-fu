from PyPDF2 import PdfFileMerger, PdfFileReader
import os

def ask(question, default_choice=None):
    actual_question = question

    if default_choice:
        actual_question = '{} [Default: {}]'.format(question, default_choice)

    print(actual_question)
    return input('>> ')


def ask_for_directory():
    return ask('What directory contains your PDFs? Please enter the absolute path.')


def is_valid_directory(directory):
    return directory and os.path.isdir(directory)


def list_files(directory, extension='pdf'):
    files = [file_name for file_name in os.listdir(directory)
             if file_name.endswith(extension)]
    files.sort()
    return files


def should_include_file(_file):
    response = None
    while not response:
        print('Include {}? [y/n]'.format(_file))
        response = input('>> ').lower()

        if response != 'y' and response != 'n':
            response = None

    return response == 'y'


def ask_for_selection(directory, files):
    return [os.path.join(directory, _file) for _file in files
            if should_include_file(_file)]


def ask_for_file_type(default='pdf'):
    file_type = ask('What is the file extension of the files you would like to combine?', default)
    return file_type if file_type else default


def ask_for_new_file_name():
    return ask('What would you like to name the combined file?')


def build_file_name(file_name, extension):
    return '{}.{}'.format(file_name, extension)


def merge(file_names, new_file_name):
    merger = PdfFileMerger()

    for file_name in file_names:
        merger.append(PdfFileReader(file_name, 'rb'))

    merger.write(new_file_name)


def ask_for_destination(file_name, default=os.getcwd()):
    destination = ask('Where would you like to save {}?'.format(file_name), default)

    if not is_valid_directory(destination):
        destination = default

    return os.path.join(destination, file_name)


def ask_where_to_work():
    directory = None

    while not is_valid_directory(directory):
        directory = ask_for_directory()

    return directory


def go_for_it(workspace, files, extension):
    selection = ask_for_selection(workspace, files)
    new_file_name = build_file_name(ask_for_new_file_name(), extension)
    destination = ask_for_destination(new_file_name, workspace)
    merge(selection, destination)
    print('Created `{}`'.format(destination))


def gogogo():
    directory = ask_where_to_work()
    extension = ask_for_file_type()
    files = list_files(directory, extension)

    if len(files) > 0:
        go_for_it(directory, files, extension)
    else:
        print('No files were found in `{}`'.format(directory))

if __name__ == '__main__':
    gogogo()
