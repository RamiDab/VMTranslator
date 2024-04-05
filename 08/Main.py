"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO,
        bootstrap: bool) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        bootstrap (bool): if this is True, the current file is the 
            first file we are translating.
    """
    # Your code goes here!

    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)
    input_file, input_extention = os.path.splitext(os.path.basename(input_file.name))
    code_writer.set_file_name(input_file)
    # if bootstrap:
    #     first_file = "@256\nD=A\n@SP\nM=D\n"
    #     output_file.write(first_file)
    #     code_writer.write_call("Sys.init", 0)

    while(parser.has_more_commands()):
        if parser.counter == parser.numoflines:
            break
        curr_line = parser.lines[parser.counter]
        curr_line = curr_line.split("//")[0].strip()
        output_file.write("// Translating -  " + curr_line + "\n")
        splitted_line = curr_line.split()
        com_type = parser.command_type()
        if com_type == "C_ARITHMETIC":
            code_writer.write_arithmetic(splitted_line[0])
        elif com_type == "C_LABEL":
            code_writer.write_label(parser.arg1())
        elif com_type == "C_GOTO":
            code_writer.write_goto(parser.arg1())
        elif com_type == "C_IF":
            code_writer.write_if(parser.arg1())
        elif com_type == "C_FUNCTION":
            code_writer.fucntion_n = parser.arg1()
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif com_type == "C_RETURN":
            code_writer.write_return()
        elif com_type == "C_CALL":
            code_writer.write_call(parser.arg1(), parser.arg2())
        else:
            code_writer.write_push_pop(splitted_line[0], splitted_line[1], splitted_line[2])
        parser.advance()



if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.

    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False