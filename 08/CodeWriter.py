"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os



class CodeWriter:
    call_counter = 0
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.i = 0
        self.out_file = output_stream
        self.input_filename = ""
        self.fucntion_n = ""


    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        self.input_filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!"
        assembly_code = ""

        if command == "add":
            assembly_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D+M\n"

        elif command == "sub":
            assembly_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M-D\n"

        elif command == "neg":
            assembly_code = "@SP\nA=M-1\nM=-M\n"

        elif command == "eq":
            assembly_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=D-M\nM=-1\n@END"+str(self.i)+"\nD;JEQ\n" \
                                                                                          "@SP\nA=M-1\nM=0\n(END"+str(self.i)+")\n"
            self.i += 1

        elif command == "lt":
            assembly_code = f"@SP\nAM=M-1\nD=M\n@GOIF{self.i}\nD;JLT\n@SP\n" \
                            f"A=M-1\nD=M\n@NOCOND{self.i}\nD;JLT\n@COND{self.i}\n" \
                            f"0;JMP\n(GOIF{self.i})\n@SP\nA=M-1\nD=M\n@COND{self.i}\n" \
                            f"D;JLT\n@NOCOND{self.i}\n0;JMP\n(COND{self.i})\n@SP\n" \
                            f"A=M-1\nD=M\n@SP\nA=M\nD=D-M\n@TRUE{self.i}\n" \
                            f"D;JLT\n@SP\nA=M-1\nM=0\n@END{self.i}\n0;JMP\n(TRUE{self.i})\n" \
                            f"@SP\nA=M-1\nM=-1\n@END{self.i}\n0;JMP\n(NOCOND{self.i})\n" \
                            f"@SP\nA=M-1\nD=M\n@TRUE{self.i}\nD;JLT\n@SP\nA=M-1\nM=0\n" + "(END" + str(self.i) + ")\n"

            self.i += 1

        elif command == "gt":
            assembly_code = f"@SP\nAM=M-1\nD=M\n@GOIF{self.i}\nD;JLT\n@SP\nA=M-1\nD=M\n@NOCOND{self.i}" \
                            f"\nD;JLT\n@COND{self.i}\n0;JMP\n(GOIF{self.i})\n@SP\nA=M-1\nD=M\n@COND{self.i}\n" \
                            f"D;JLT\n@NOCOND{self.i}\n0;JMP\n(COND{self.i})\n@SP\nA=M-1\nD=M\n@SP\nA=M\nD=D-M\n@TRUE{self.i}\n" \
                            f"D;JGT\n@SP\nA=M-1\nM=0\n@END{self.i}\n0;JMP\n(TRUE{self.i})\n" \
                            f"@SP\nA=M-1\nM=-1\n@END{self.i}\n0;JMP\n(NOCOND{self.i})\n" \
                            f"@SP\nA=M-1\nD=M\n@TRUE{self.i}\nD;JGT\n" \
                            "@SP\nA=M-1\nM=0\n" + "(END" + str(self.i) + ")\n"
            self.i += 1

        elif command == "and":
            assembly_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M&D\n"
        elif command == "or":
            assembly_code = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M|D\n"
        elif command == "not":
            assembly_code = "@SP\nA=M-1\nM=!M\n"
        elif command == "shiftleft":
            assembly_code = "@SP\nA=M-1\nM=M<<\n"
        elif command == "shiftright":
            assembly_code = "@SP\nA=M-1\nM=M>>\n"

        self.out_file.write(assembly_code)

    def write_push_pop(self, command: str, segment: str, count: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        assembly_code = ""
        if command == "push":
            assembly_code = self.write_push(segment, count)
        elif command == "pop":
            assembly_code = self.write_pop(segment, count)
        self.out_file.write(assembly_code)

    def write_push(self,seg : str, i : int) -> str:
        result = ""

        if seg == "constant":
            result = f"@{i}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        elif seg == "pointer":
            result = f"@{i}\nD=A\n@3\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        elif seg == "temp":
            result = f"@{i}\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        elif seg == "local":
            result = f"@LCL\nD=M\n@{i}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        elif seg == "argument":
            result = f"@ARG\nD=M\n@{i}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        elif seg == "this":
            result = f"@{i}\nD=A\n@THIS\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        elif seg == "that":
            result = f"@{i}\nD=A\n@THAT\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        elif seg == "static":
            result = "@" + self.input_filename + "." + str(i) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

        return result

    def write_pop(self, seg: str, i: int) -> str:
        result = ""
        if seg == "pointer":
            result += f"@{i}\nD=A\n@3\nD=A+D\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@R14\nA=M\nM=D\n"

        elif seg == "temp":
            result += f"@{i}\nD=A\n@5\nD=D+A\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@R14\nA=M\nM=D\n"

        elif seg == "local":
            result += f"@{i}\nD=A\n@LCL\nD=D+M\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@R14\nA=M\nM=D\n"

        elif seg == "argument":
            result += f"@{i}\nD=A\n@ARG\nD=D+M\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@R14\nA=M\nM=D\n"

        elif seg == "this":
            result += f"@{i}\nD=A\n@THIS\nD=D+M\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@R14\nA=M\nM=D\n"

        elif seg == "that":
            result += f"@{i}\nD=A\n@THAT\nD=D+M\n@R14\nM=D\n@SP\nAM=M-1\nD=M\n@R14\nA=M\nM=D\n"

        elif seg == "static":
            result += "@SP\nAM=M-1\nD=M\n@" + self.input_filename + "." + str(i) + "\nM=D\n"

        return result

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        result = f"({self.fucntion_n}${label})\n"
        self.out_file.write(result)

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        result = f"@{self.fucntion_n}${label}\n0;JMP\n"
        self.out_file.write(result)

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        result = f"@SP\nM=M-1\nA=M\nD=M\n@{self.fucntion_n}${label}\nD;JNE\n"
        self.out_file.write(result)

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.fucntion_n = function_name
        function_write = f"({function_name})\n"
        self.out_file.write(function_write)
        for k in range(n_vars):
            self.out_file.write(self.write_push("constant", 0))

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        return_address = f"@{function_name}$ret.{CodeWriter.call_counter}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.out_file.write(return_address)

        # push LCL              // saves LCL of the caller
        local_seg_push = "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.out_file.write(local_seg_push)

        # push ARG              // saves ARG of the caller
        arg_seg_push = "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.out_file.write(arg_seg_push)

        # push THIS             // saves THIS of the caller
        this_seg_push = "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.out_file.write(this_seg_push)

        # push THAT             // saves THAT of the caller
        that_seg_push = "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.out_file.write(that_seg_push)

        # ARG = SP-5-n_args     // repositions ARG
        arg_update = f"@SP\nD=M\n@{n_args}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n"
        self.out_file.write(arg_update)

        # LCL = SP              // repositions LCL
        local_update = "@SP\nD=M\n@LCL\nM=D\n"
        self.out_file.write(local_update)

        # goto function_name    // transfers control to the callee
        Goto_Func = f"@{function_name}\n0;JMP\n"
        self.out_file.write(Goto_Func)

        # (return_address)      // injects the return address label into the code
        inject_retadd = f"({function_name}$ret.{CodeWriter.call_counter})\n"
        self.out_file.write(inject_retadd)

        CodeWriter.call_counter += 1

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:

        # frame = LCL                   // frame is a temporary variable
        endframe = "@LCL\nD=M\n@R14\nM=D\n"   # Endframe address will be saved in R14.
        self.out_file.write(endframe)

        # return_address = *(frame-5)   // puts the return address in a temp var
        re_add = "@5\nAD=D-A\nD=M\n@R15\nM=D\n"    # the return address will be saved in R15.
        self.out_file.write(re_add)

        # *ARG = pop()                  // repositions the return value for the caller
        popping_arg = "@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n"
        self.out_file.write(popping_arg)

        # SP = ARG + 1                  // repositions SP for the caller
        updating_sp = "@ARG\nD=M+1\n@SP\nM=D\n@R14\nAM=M-1\nD=M\n"
        self.out_file.write(updating_sp)

        # THAT = *(frame-1)             // restores THAT for the caller
        that_update = "@THAT\nM=D\n@R14\nAM=M-1\nD=M\n"
        self.out_file.write(that_update)

        # THIS = *(frame-2)             // restores THIS for the caller
        this_update = "@THIS\nM=D\n@R14\nAM=M-1\nD=M\n"
        self.out_file.write(this_update)

        # ARG = *(frame-3)              // restores ARG for the caller
        argument_update = "@ARG\nM=D\n@R14\nAM=M-1\nD=M\n"
        self.out_file.write(argument_update)

        # LCL = *(frame-4)              // restores LCL for the caller
        local_update = "@LCL\nM=D\nA=M\nD=M\n"
        self.out_file.write(local_update)

        # goto return_address           // go to the return address
        final_jump = "@R15\nA=M\n0;JMP\n"
        self.out_file.write(final_jump)

