#!/usr/bin/python


# This is a template lldb python script for adding a new function
# I add to python path first:
# export PYTHONPATH="/Users/bbarrows/python:/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Resources/Python:$PYTHONPATH"
# and run lldb:
# /Applications/Xcode.app/Contents/Developer/usr/bin/lldb
# command script import  /Users/bbarrows/python/ex.py

import lldb
import optparse
import shlex

def create_options():
    """Parse the options passed to the command. 
    Also provides the description string that's used as
    the command's help string.
    """
    usage = "usage: %prog [options] <filter> <variable_name>"
    description = '''This command will run the ex function, TestFunc.

Example:
%prog '.[]|{firstName, lastName}' jsonStr
%prog '.[]|select(.id=="f9a5282e-523f-4b83-a6ca-566e3746a4c7").schools[1].\
school.mainLocation.address.city' body
'''
    parser = optparse.OptionParser(
        description=description,
        prog='ex',
        usage=usage)
    parser.add_option(
        '-c',
        '--compact',
        action='store_true',
        dest='compact',
        help='compact instead of pretty-printed output',
        default=False)
    parser.add_option(
        '-S',
        '--sort',
        action='store_true',
        dest='sort',
        help='sort keys of objects on output',
        default=False)
    return parser


def TestFunc(debugger, command, result, internal_dict):
    # Use the Shell Lexer to properly parse up command options just like a
    # shell would
    command_args = shlex.split(command)
    parser = create_options()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        # if you don't handle exceptions, passing an incorrect argument to the 
        # OptionParser will cause LLDB to exit (courtesy of OptParse dealing 
        # with argument errors by throwing SystemExit)
        result.SetError("option parsing failed")
        return

    if options.compact:
        result.AppendMessage("compact string")

    result.AppendMessage("Before hey")
    try:
        # in a command - the lldb.* convenience variables are not to be used
        # and their values (if any) are undefined
        # this is the best practice to access those objects from within a command
        target = debugger.GetSelectedTarget()
        process = target.GetProcess()
        thread = process.GetSelectedThread()
        frame = thread.GetSelectedFrame()
        if not frame.IsValid():
            return "no frame here"
    except:
        result.SetError("Error getting target, process, thread or frame")
    result.AppendMessage("hey")


def __lldb_init_module(debugger, dict):
    # This initializer is being run from LLDB in the embedded command interpreter
    # Make the options so we can generate the help text for the new LLDB
    # command line command prior to registering it with LLDB below
    parser = create_options()
    TestFunc.__doc__ = parser.format_help()
    
    print(TestFunc.__doc__)

    # Add any commands contained in this module to LLDB
    debugger.HandleCommand('command script add -f ex.TestFunc ex')

    print("""The "ex" command has been installed, type "help ex" or "ex --help" for detailed help.""")

