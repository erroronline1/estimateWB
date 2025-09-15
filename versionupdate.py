import sys
import re
import os
from datetime import datetime

def helparg():
    print(f'''
usage: versionupdate.py [ -h  | --help ]
                        [ -v  | --version ] VERSION
                        [ -d  | --description ] DESCRIPTION

updates the workbench version number and description on all relevant issued places like
* package.xml
* pyproject.toml

not in the readme though
''')
    
def update(version, description):
    version = version.strip() if version else version
    description = description.strip() if description else description

    root_path = os.path.dirname(os.path.realpath(__file__))
    root_files = os.listdir(root_path)

    '''
    # detect workbench in calling directory to process occasional containes files to alter, if any
    try:
        wb_path = os.listdir(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/freecad'))[0]
    except:
        wb_path = None
    '''

    if 'package.xml' in root_files:
        path = os.path.realpath(root_path + '/package.xml')
        if version:
            xmlversion = version.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
            rewrite(path, r'<version>.+?<\/version>', '<version>' + xmlversion + '</version>')
        if description:
            xmldescription = description.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
            rewrite(path, r'<description>.+?<\/description>', '<description>' + xmldescription + '</description>')  
        rewrite(path, r'<date>.+?<\/date>', '<date>' + datetime.today().strftime('%Y-%m-%d') + '</date>')
        print(path + ' updated')
    if 'pyproject.toml' in root_files:
        path = os.path.realpath(root_path + '/pyproject.toml')
        if version:
            rewrite(path, r'version\s{0,}=\s{0,}["\'].+?["\']', 'version = "' + version + '"')
        if description:
             rewrite(path, r'description\s{0,}=\s{0,}["\'].+?["\']', 'description = "' + description + '"')
        print(path + ' updated')

    if version:
        print(f'set to version "{version}"', end = ' with ' if description else None)
    if description:
        print(f'description "{description}"')
    print ('please check if everything fits')

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
        # this should come last after all other patterns have been detected and subtracted from the arguments
        'd': '((?:--description|-d)[:\\s]+)(.+)'
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
    if params:
        print ("params could not be fully resolved, aborting:", params)

    if version or description:
        update(version, description)
    else:
        helparg()