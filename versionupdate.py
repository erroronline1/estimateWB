import sys
import re
import os
from datetime import datetime

def helparg(workbench):
    print(f'''
usage: versionupdate.py [ -h  | --help ]
                        [ -v  | --version ] VERSION
                        [ -d  | --description ] DESCRIPTION

updates the workbench version number and description on all relevant issued places like
* freecad/{workbench}/version.py
* manifest.ini
* package.xml
* setup.py

because it affects so many different places. not in the readme though

called from the root folder of the workbench it detects the name within
the freecad-directory on its own. only quoted values are replaced within py files.
''')
    
def update(workbench, version, description):
    version = version.strip() if version else version
    description = description.strip() if description else description

    root_path = os.path.dirname(os.path.realpath(__file__))
    wb_path = os.path.realpath(current_path + '/freecad/' + workbench)

    root_files = os.listdir(root_path)
    wb_files = os.listdir(wb_path)

    if 'manifest.ini' in root_files:
        path = os.path.realpath(current_path + '/manifest.ini')
        if version:
            rewrite(path, r'version=.+', 'version=' + version)
        if description:
            rewrite(path, r'description=.+', 'description=' + description)
        print(path + ' bumped')
    if 'package.xml' in root_files:
        path = os.path.realpath(current_path + '/package.xml')
        if version:
            rewrite(path, r'<version>.+?<\/version>', '<version>' + version + '</version>')
        if description:
             rewrite(path, r'<description>.+?<\/description>', '<description>' + description + '</description>')  
        rewrite(path, r'<date>.+?<\/date>', '<date>' + datetime.today().strftime('%Y-%m-%d') + '</date>')
        print(path + ' bumped')
    if 'setup.py' in root_files:
        path = os.path.realpath(current_path + '/setup.py')
        if version:
            # does not replace imported variables by searching for literal values within quotes only
            rewrite(path, r'version\s{0,}=\s{0,}["\'].+?["\']', 'version="' + version + '"')
        if description:
             rewrite(path, r'description\s{0,}=\s{0,}["\'].+?["\']', 'description="' + description + '"')
        rewrite(path, r'<date>.+?<\/date>', '<date>' + datetime.today().strftime('%Y-%m-%d') + '</date>')
        print(path + ' bumped')

    if 'version.py' in wb_files:
        path = os.path.realpath(current_path + '/freecad/' + workbench + '/version.py')
        if version:
            rewrite(path, r'__version__ = ".+?"', '__version__ = "' + version + '"')
        print(path + ' bumped')
    print('please check if everything fits')

def rewrite(path, re_search, re_replace):
    # read file
    with open(path, 'r') as file:
        filedata = file.read()
    # replace target string
    filedata = re.sub(re_search, re_replace, filedata)
    # write file
    with open(path, 'w') as file:
        file.write(filedata)

if __name__ == '__main__':
    # argument handler
    # omit first argument (scriptname)
    sys.argv.pop(0)
    # find and assign option arguments, strip arguments, remainder should be string
    options = {
        'h': '--help|-h',
        'v': '((?:--version|-v)[:\\s]+)([^\s]+)',
        'd': '((?:--description|-d)[:\\s]+)([^\s]+)'
    }
    params = ' '.join(sys.argv) + ' '
    version = None
    description = None
    for opt in options:
        arg = re.findall(options[opt], params, re.IGNORECASE)
        if opt == 'v' and bool(arg):
            version = arg[0][1]
            params = params.replace(''.join(arg[0]), '')
        if opt == 'd' and bool(arg):
            description = arg[0][1]
            params = params.replace(''.join(arg[0]), '')

    workbench = None
    # detect workbench in calling directory
    current_path = os.path.dirname(os.path.realpath(__file__))
    if 'freecad' in os.listdir(current_path):
        workbench = os.listdir(os.path.realpath(current_path + '/freecad'))[0]
    
    if workbench and (version or description):
        update(workbench, version, description)
    else:
        helparg(workbench)