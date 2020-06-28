# COMP9319 UNSW 20T2
# Assignment 1 tests
# Author: Christopher Lord

import filecmp
import os
import subprocess
import sys

# Location of test cases
TEST_DIR = 'tests'

def red_text(message):
    return f'\033[0;31m{message}\033[0m'


def green_text(message):
    return f'\033[0;32m{message}\033[0m'


def blue_text(message):
    return f'\033[0;36m{message}\033[0m'


def red_background_text(message):
    return f'\033[41m{message}\033[0m'


def green_background_text(message):
    return f'\033[42m{message}\033[0m'


def find_cases():
    # Check that we have valid test cases to run
    assert os.path.isdir(TEST_DIR), f'Expected {blue_text("tests")} directory to exist'
    sources = sorted([file for file in os.listdir(TEST_DIR) if file.endswith('-source.txt')])
    assert len(sources), 'Expected at least one test case'
    return sorted(sources)


def check_make():
    assert os.path.exists('makefile'), f'Expected {blue_text("makefile")} in current directory'
    try:
        output = subprocess.run('make', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        print(f'Expected make to run without error')
        sys.exit(0)
    assert os.path.exists('aencode'), f'Expected {blue_text("aencode")} in current directory'
    assert os.path.exists('adecode'), f'Expected {blue_text("adecode")} in current directory'


def clear_cases():
    # Cleanup output files in test directory
    for file in os.listdir(TEST_DIR):
        if file.endswith('-output.txt') or file.endswith('-encoded.txt'):
            os.remove(os.path.join(TEST_DIR, file))


def check_case(case):
    # Execute a test case
    passed = True

    case_number = case[:3]
    source_path = os.path.join(TEST_DIR, case)
    encode_path = os.path.join(TEST_DIR, f'{case_number}-encoded.txt')
    output_path = os.path.join(TEST_DIR, f'{case_number}-output.txt')

    print(f'Test {case_number}.. ', end='')

    # Generate encoded output
    try:
        output = subprocess.run(f'./aencode < {source_path} > {encode_path}', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        print(e)
        sys.exit(0)

    assert os.path.isfile(encode_path), 'Expected encoded file'

    # Generate output
    try:
        output = subprocess.run(f'./adecode < {encode_path} > {output_path}', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        print(e)
        sys.exit(0)

    assert os.path.isfile(output_path), 'Expected output file'

    # Check input and output are identical
    if not filecmp.cmp(source_path, output_path):
        passed = False

    return passed


def main():
    # Run makefile
    check_make()

    # Clear old cases
    clear_cases()

    # Run tests
    failed = 0
    completed = 0
    for case in find_cases():

        if not check_case(case):
            print(red_text('FAILED'))
            failed += 1
        else:
            print(green_text('PASS'))

        completed += 1

    if not failed:
        print(green_background_text(f'{"All test cases passed!":^60}'))
    else:
        error_str = f'Failed {failed} of {completed} tests'
        print('\n' + red_background_text('{0:^60}'.format(error_str)))

    stat_str = f'Completed: {completed}  Passed: {completed - failed}  Failed: {failed}'
    print(f'\n{stat_str:^60}\n')
 

if __name__ == '__main__':
    main()













