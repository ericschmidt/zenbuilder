##
# zenbuilder - JavaScript Build Tool
#
# Really just recursively concatenates JS files in a directory and its subdirectories.
# Eric Schmidt 2016
# eschmidt.co
##

import httplib
import os
import sys
import urllib

## CONSTANTS

# Messages
USAGE = 'Usage: zen -i <root_dir> -o <output_file>\n\nType zen -h for help'
HELP = '''zenbuilder - JavaScript build tool by Eric Schmidt (eschmidt.co)

Usage: zen -i <root_dir> -o <output_file> [-m] [-v] [-h]

Detail:
-i, --in  <root_dir>        Specify the root directory for JavaScript source
-o, --out <output_file>     Specify the name of the concatenated output file
-m, --minify                Also generate a minified JS file in the same location as the output file
-v, --verbose               Enable verbose mode to print extra information about build progress
-h, --help                  Show this help'''

START_MESSAGE = "Searching folder '%s' for source files..."
ADDING_MESSAGE = '+ Adding %s'
IGNORING_MESSAGE = '- Ignoring %s'
MINIFYING_MESSAGE = "Creating minified file '%s'..."
COMPLETE_MESSAGE = "Build finished to '%s'"
NOT_A_DIR_MESSAGE = "The folder '%s' could not be found."

# Flags
START_DIR_FLAG = ('-i', '--in')
OUTPUT_FLAG = ('-o', '--out')
MINIFY_FLAG = ('-m', '--minify')
VERBOSE_FLAG = ('-v', '--verbose')
HELP_FLAG = ('-h', '--help')

# Config
CONFIG_FILE = '.zenconfig'
CONFIG_SEPARATOR = '@'
CONFIG_START_DIR = 'root_dir'
CONFIG_OUTPUT_FILE = 'output_file'
CONFIG_GENERATE_MINIFIED = 'minify'
CONFIG_VERBOSE = 'verbose'
CONFIG_IGNORE_EXTENSIONS = 'ignore'

# Other
EXTENSION_JS = '.js'

## HELPERS
def die(message):
    print message
    exit()

def minify(code):
    # Uses Google Closure Compiler API
    params = urllib.urlencode([
        ('js_code', code),
        ('output_info', 'compiled_code')
    ])
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    connection = httplib.HTTPConnection('closure-compiler.appspot.com')
    connection.request('POST', '/compile', params, headers)
    minified = connection.getresponse().read()
    connection.close()
    return minified

def generateMinFilename(filename):
    MIN = 'min'
    parts = filename.split('.')
    if len(parts) > 1:
        parts.insert(len(parts)-1, MIN)
    else:
        parts.append(MIN)
    return '.'.join(parts)

## MAIN

# Arguments
startDir = None
outputFilename = None
showHelp = False
generateMinified = False
verbose = False
ignoreExtensions = tuple()

# Read arguments from config file if possible
if os.path.isfile(CONFIG_FILE):
    config = []
    with open(CONFIG_FILE, 'r') as cfg:
        config = cfg.read().split(CONFIG_SEPARATOR)
    for block in config:
        parts = block.strip().split()
        if len(parts) > 0:
            if parts[0] == CONFIG_START_DIR:
                if len(parts) > 1: startDir = parts[1]
            elif parts[0] == CONFIG_OUTPUT_FILE:
                if len(parts) > 1: outputFilename = parts[1]
            elif parts[0] == CONFIG_GENERATE_MINIFIED:
                generateMinified = True
            elif parts[0] == CONFIG_VERBOSE:
                verbose = True
            elif parts[0] == CONFIG_IGNORE_EXTENSIONS:
                ignoreExtensions = tuple(parts[1:])

# Then override with command-line args
for i in range(len(sys.argv)):
    # Binary flags
    if sys.argv[i] in HELP_FLAG:
        showHelp = True
    elif sys.argv[i] in MINIFY_FLAG:
        generateMinified = True
    elif sys.argv[i] in VERBOSE_FLAG:
        verbose = True
    # Flags with one argument
    if len(sys.argv) > i+1:
        if sys.argv[i] in START_DIR_FLAG:
            startDir = sys.argv[i+1]
        elif sys.argv[i] in OUTPUT_FLAG:
            outputFilename = sys.argv[i+1]

if showHelp:
    die(HELP)

if startDir is None or outputFilename is None:
    die(USAGE)

if not os.path.isdir(startDir):
    die(NOT_A_DIR_MESSAGE % startDir)

output = open(outputFilename, 'w')

# Walk & concatenate
print START_MESSAGE % startDir
for (root, dirs, files) in os.walk(startDir):
    for filename in files:
        filepath = os.path.join(root, filename)
        if filename.endswith(ignoreExtensions):
            if verbose: print IGNORING_MESSAGE % filepath
        elif filename.endswith(EXTENSION_JS):
            if verbose: print ADDING_MESSAGE % filepath
            with open(filepath, 'r') as f:
                output.write(f.read())
                output.write('\n')
output.close()

if generateMinified:
    minFilename = generateMinFilename(outputFilename)
    if verbose: print MINIFYING_MESSAGE % minFilename
    minFile = open(minFilename, 'w')
    with open(outputFilename, 'r') as code:
        minFile.write(minify(code.read()))
    minFile.close()

print COMPLETE_MESSAGE % outputFilename
