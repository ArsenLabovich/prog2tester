import shutil
import subprocess
import os
import re
import time
import argparse
from pathlib import Path

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

DEFAULT_C_FILENAME = 'main.c'

parser = argparse.ArgumentParser(description='Run tests for C program.')
parser.add_argument('-s', '--show-diff', default=False, action='store_true',
                    help='Show differences between expected and actual output')
args = parser.parse_args()
show_diff = args.show_diff


def normalize_spaces(line):
    return re.sub(r' {2,}', ' ', line).rstrip()


def highlight_differences(expected, actual):
    print("\n\033[91mACTUAL OUTPUT:\033[0m\n")

    for exp_line, act_line in zip(expected, actual):
        exp_parts = re.split(r'(\s+)', exp_line)
        act_parts = re.split(r'(\s+)', act_line)

        highlighted_line = []
        for exp, act in zip(exp_parts, act_parts):
            if exp == act:
                highlighted_line.append(act)
            else:
                highlighted_line.append(RED + act + RESET)

        print("".join(highlighted_line))
    print("\n\n\n\033[92mEXPECTED OUTPUT:\033[0m\n")
    for exp_line in expected:
        exp_parts = re.split(r'(\s+)', exp_line)
        highlighted_line = []
        for exp in exp_parts:
            highlighted_line.append(GREEN + exp + RESET)

        print("".join(highlighted_line))


def checkFilesAndFolders():
    if not os.path.exists('tests'):
        print("\033[91mTests folder not found\033[0m")
        print("\033[93mPlease read README.md file and follow instructions\033[0m")
        exit(1)
    if not os.path.exists(DEFAULT_C_FILENAME):
        print("\033[91mC file not found\033[0m")
        print("\033[93mPlease read README.md file and follow instructions\033[0m")
        exit(1)
    if not shutil.which("gcc"):
        print("\033[91mGCC compiler not found\033[0m")
        print("\033[93mPlease install GCC compiler and ensure it is in your PATH\033[0m")
        exit(1)
    print("\033[92mTester found all necessary files and GCC\033[0m")


def compile_c_file(c_file_path):
    compile_command = ['gcc', c_file_path, '-o', 'output']
    try:
        result = subprocess.run(compile_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\033[91mCompilation failed...\033[0m")
            print(f"\033[93m{result.stderr.strip()}\033[0m")
            return False
    except FileNotFoundError:
        print("\033[91mGCC compiler not found\033[0m")
        return False
    except subprocess.SubprocessError as e:
        print(f"\033[91mAn error occurred while compiling: {e}\033[0m")
        return False
    return True


def run_c_program(c_input_data_path):
    try:
        with open(c_input_data_path, 'r') as f:
            c_input_text = f.read()
    except FileNotFoundError:
        print(f"\033[91mInput file {c_input_data_path} not found\033[0m")
        return ""
    except IOError as e:
        print(f"\033[91mError reading input file {c_input_data_path}: {e}\033[0m")
        return ""

    run_command = ['./output']
    try:
        result = subprocess.run(run_command, input=c_input_text, capture_output=True, text=True, timeout=5)
        return result.stdout
    except subprocess.TimeoutExpired:
        print("\033[91mExecution timed out\033[0m")
        return ""
    except subprocess.SubprocessError as e:
        print(f"\033[91mAn error occurred while running the program: {e}\033[0m")
        return ""


def run_tests_in_folder(folder):
    input_data_paths = [os.path.join(folder, f'input{i}.txt') for i in range(1, len(os.listdir(folder)) // 2 + 1)]
    expected_output_paths = [os.path.join(folder, f'output{i}.txt') for i in range(1, len(os.listdir(folder)) // 2 + 1)]

    counter = 1
    summary = []

    for input_data_path, expected_output_path in zip(input_data_paths, expected_output_paths):
        with open(expected_output_path, 'r') as file:
            expected_output = file.readlines()
        c_program_output = run_c_program(input_data_path).splitlines()

        expected_output_normal = [normalize_spaces(line) for line in expected_output]
        c_program_output_normal = [normalize_spaces(line) for line in c_program_output]

        if expected_output_normal == c_program_output_normal:
            print(f"\033[92mTest passed in {folder} TEST#{counter}\033[0m")
            summary.append(f"\033[92mTest passed in {folder} TEST#{counter}\033[0m")
        else:
            print(f"\033[91mTest failed in {folder} TEST#{counter}\033[0m")
            summary.append(f"\033[91mTest failed in {folder} TEST#{counter}\033[0m")
            if show_diff:
                print(f"\033[93mInput data: {input_data_path}\033[0m")
                print(f"\033[93mExpected output: {expected_output_path}\033[0m\n\n")
                highlight_differences(expected_output, c_program_output)
                for seconds in range(2, 0, -1):
                    print(f"\033[91mTesting will continue in {seconds} seconds...\033[0m", end="\r", flush=True)
                    time.sleep(1)
        counter += 1
        time.sleep(0.1)
    return summary


def main():
    checkFilesAndFolders()

    test_folders = [Path('tests') / f'scenar_{i}' for i in range(1, len(os.listdir('tests')) + 1)]

    if not compile_c_file("./" + DEFAULT_C_FILENAME):
        print("\033[91mPossible errors in the code. Please check the code and try again.\033[0m\n"
              "\033[91mMake sure that you use the same compiler in the terminal and in the IDE.\033[0m\n"
              "\033[91mTester will able to compile main.c file, if you can compile it using gcc main.c -o output\033[0m\n")
        exit(1)

    all_summaries = []
    for folder in test_folders:
        summary = run_tests_in_folder(folder)
        all_summaries.extend(summary)
        print("\n")

    if show_diff:
        for line in all_summaries:
            print(line)


if __name__ == "__main__":
    main()
