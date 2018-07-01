# $Id: os_utils.py,v 1.4 2004/03/01 22:07:53 lliabraa Exp $
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

import os
import sys
import commands
import getopt
import string
import stat
import tempfile

#---------------------------------------------------------------------
def build_opt_description(options_supported):
    
    opt_description = ''
    for option_name in options_supported.keys():
                
        if options_supported[option_name]['type'] == 'required':
            opt_description = opt_description + '-' + options_supported[option_name]['abbreviation']
            opt_description = opt_description + ' <' + option_name + '> '
        else:
            opt_description = opt_description + '[-' + options_supported[option_name]['abbreviation']
            if options_supported[option_name]['argument_required']:
                opt_description = opt_description + ' <' + option_name + '>] '
            else:
                opt_description = opt_description + '] '

    return opt_description
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def get_cmd_opts_and_args(cmd_line, options_supported, extra_cmd_description='files...'):
    '''
    '''

    short_options = ''
    long_option_list = []

    opt_description = build_opt_description(options_supported)
    
    for option_name in options_supported.keys():
        
        options_supported[option_name]['occurs'] = 0
        
        short_options = short_options + options_supported[option_name]['abbreviation']
        
        if options_supported[option_name]['type'] == 'required':
            short_options = short_options + ':'        
            long_option_name = option_name + '='
        else:
            long_option_name = option_name
            
        long_option_list.append(long_option_name)

    try:
        
        opts, args = getopt.getopt(cmd_line[1:],short_options,long_option_list)
        
        for option_name in options_supported.keys():
                
            if options_supported[option_name]['type'] == 'required':

                option_on_cmd_line = 0
                    
                for option in opts:
                    
                    name, value = option
                    
                    if name == '-' + options_supported[option_name]['abbreviation'] or name == '--' + option_name:

                        option_on_cmd_line = 1

                        if options_supported[option_name]['argument_required']:
                            options_supported[option_name]['value'] = value
                        else:
                            options_supported[option_name]['value'] = 1
                        break

                if not option_on_cmd_line:
                    print 'missing required option: ' + '-' + options_supported[option_name]['abbreviation'] + ' <' + option_name + '>'
                    if extra_cmd_description != None:
                        print 'usage: ' + cmd_line[0] + ' ' + opt_description + extra_cmd_description
                    else:
                        print 'usage: ' + cmd_line[0] + ' ' + opt_description

                    return 'error', opts, args

        for option in opts: 

            name, value = option
            
            for option_name in options_supported.keys():

                if name == '-' + options_supported[option_name]['abbreviation'] or name == '--' + option_name:

                    if options_supported[option_name]['argument_required']:
                        options_supported[option_name]['value'] = value
                    else:
                        options_supported[option_name]['value'] = 1
                                                
                    if not options_supported[option_name].has_key('occurs'):
                        options_supported[option_name]['occurs'] = 1
                    else:
                        options_supported[option_name]['occurs'] = options_supported[option_name]['occurs'] + 1
                    break

        for option_name in options_supported.keys():
            if options_supported[option_name]['occurs'] > options_supported[option_name]['max_occurs']:
                print 'exceed option repetition of ' + `options_supported[option_name]['max_occurs']` + ': ' + '-' + options_supported[option_name]['abbreviation'] + ' <' + option_name + '>'
                if extra_cmd_description != None:
                    print 'usage: ' + cmd_line[0] + ' ' + opt_description + extra_cmd_description
                else:
                    print 'usage: ' + cmd_line[0] + ' ' + opt_description
                        
                return 'error', opts, args
                    
        return 'success', opts, args

    except getopt.error:

        if extra_cmd_description != None:
            print 'usage: ' + cmd_line[0] + ' ' + opt_description + extra_cmd_description
        else:
            print 'usage: ' + cmd_line[0] + ' ' + opt_description
                
        return 'error', None, None
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def su_exec(command,shell=None):

    print 'Enter root password:'

    if shell != None:
        shell_flag = '-s'
    else:
        shell_flag = ''
        shell = ''

    status, output = commands.getstatusoutput('su -c "%s" %s %s' % (command,shell_flag,shell))
        
    if status != 0:
        return ('error', output)
    else:
        return ('success', output)
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def file_type(filename):

    filename=string.replace(filename,'"','?')
    #print "<BR>"
    #print '''file -b "%s"''' % (filename)
    #print "<BR>"
    status, output = commands.getstatusoutput('''file -b "%s"''' % (filename))
    
    if status != 0:
        return ('error', output, None)
    else:
        if output[:3] == 'Zip':
            return ('success', 'ZIP', 'zipicon.gif')
        elif output[:3] == 'tar' or output[:7] == 'GNU tar' or output[:9] == 'POSIX tar':
            return ('success', 'TAR', 'tar.gif')
        elif output[:4] == 'gzip':
            return ('success', 'GZIP', 'zipicon.gif')
        elif output[:4] == 'HTML':
            return ('success', 'HTML', 'htmlicon.gif')
        elif output[:3] == 'GIF':
            return ('success', 'GIF', 'gificon.gif')
        elif output[:16] == 'Rich Text Format':
            return ('success', 'RTF', 'rtf.gif')
        elif output[:4] == 'JPEG':
            return ('success', 'JPEG', 'image2.gif')
        elif output[:3] == 'ELF':
            return ('success', 'BIN', 'binary.gif')
        elif output[:4] == 'mail':
            return ('success', 'Mail', 'unknown.gif')
        elif output[:10] == 'PostScript':
            returrn ('success', 'PostScript', 'ps.gif')
        elif output[:5] == 'ASCII':
            return ('success', 'ASCII text', 'txticon.gif')
        elif output == 'Microsoft Office Document':
            root, extension = os.path.splitext(filename)
            if extension == '.doc':
                return ('success', 'MS Word', 'wordicon.gif')
            elif extension == '.xls':
                return ('success', 'MS Excel', 'xlsicon.gif')
            elif extension == '.ppt':
                return ('success', 'MS Power Point', 'ppticon.gif')
            else:
                return ('success', 'MS Office', 'unknown.gif')
        elif output[:3] == 'PDF':
            return ('success', 'PDF', 'pdficons.gif')
        else:
            return ('error', 'Unknown', 'unknown.gif')
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def super_chown(directory_name,username,groupname):

    status, output = commands.getstatusoutput('chown -R %s.%s %s' % (username,groupname,directory_name))
        
    if status != 0:
        return ('error', output)
    else:
        return ('success', output)
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def super_remove(directory_name):
    
    status, output = commands.getstatusoutput('rm -rf %s' % (directory_name))
    
    if status != 0:
        return ('error', output)
    else:
        return ('success', output)
#---------------------------------------------------------------------

        
#---------------------------------------------------------------------
def tar_extract(tarball_name, verbose=1, echoOnError=0):
    '''
    tarball_name -> string consisting of the name of the tarball to extract
    verbose -> integer consisting of 1 for verbosity, 0 for no verbosity
    echoOnError -> echo to stdout error output
    '''

    if verbose:
        verbose_flag = 'v'
        
    else:
        verbose_flag = ''

    if os.path.exists(tarball_name):

        status, output = commands.getstatusoutput('tar x%sf %s' % (verbose_flag, tarball_name))

        if status != 0:

            if echoOnError:
                print 'Error: ' + status + ', ' +  output
                        
            return ('error', output)
            
        else:
            
            return ('success', output)

    else:
        return ('error','tarball %s does not exist' % (tarball_name))
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def tar_create(tarball_name, files_to_tar, verbose=1, echoOnError=0):
    '''
    tarball_name -> string consisting of the name of the tarball to create
    verbose -> integer consisting of 1 for verbosity, 0 for no verbosity
    echoOnError -> echo to stdout error output
    files_to_tar -> list consisting of strings where each string is a
    filename or directory name
    '''

    if verbose:
        verbose_flag = 'v'
        
    else:
        verbose_flag = ''
        
    status, output = commands.getstatusoutput('tar c%sf %s %s' % (verbose_flag, tarball_name, string.join(files_to_tar)))
    
    if status != 0:
            
        if echoOnError:
            print 'Error: ' + status + ', ' +  output
            
        return ('error', output)
        
    else:
        
        if verbose_flag:
            print 'Results of tar create command:'
            print output
            
        return ('success', output)
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def getenv(name):

    if os.environ.has_key(name):
        return ('success', os.environ[name])
    else:
        return ('error', None)
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def setenv(name, value, overrideIfSet=0):

    if not os.environ.has_key(name):
        print 'The environment variable %s is not set,' % (name)
        print 'Defaulting to ' + value
        os.environ[name] = value
        return ('success', 'variable created and value set')
    
    else:
        
        if overrideIfSet:
            print 'Previous value of environment variable %s is %s' %(name, os.environ[name])
            print 'Overriding previous value of environment variable %s to %s' % (name, value)
            os.environ[name] = value
            return ('success', 'value overriden')
        else:
            return ('success', 'value not changed')
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def gunzip(filename,force=1,echoOnError=0):

    if os.path.exists(filename):
        
        if filename[-3:] == '.gz' or filename[-2:] == '.Z':
            
            if force:
                force_switch = '-f'
            else:
                force_switch = ''
                        
            status, output = commands.getstatusoutput('gzip -d %s %s' % (force_switch, filename))

            if status != 0:
                if echoOnError:
                    print 'Error: ' + status + ', ' +  output
                    
                return ('error', output)
                
            else:
                return ('success', output)

        else:
            return ('error', 'file does not have a suffix of .gz or .Z')

    else:
        return ('error','file does %s not exist' % (filename))
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def unzip(filename,echoOnError=0):

    if os.path.exists(filename):
        
        if filename[-4:] == '.zip':
            
            status, output = commands.getstatusoutput('unzip -o %s' % (filename))

            if status != 0:
                if echoOnError:
                    print 'Error: ' + status + ', ' +  output
                    
                return ('error', output)
                
            else:
                return ('success', output)
                
        else:
            return ('error', 'file does not have a suffix of .zip')

    else:
        return ('error','file does %s not exist' % (filename))
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def gzip(filename,force=1,echoOnError=0):

    if os.path.exists(filename):
        if force:
            force_switch = '-f'
        else:
            force_switch = ''
                        
        status, output = commands.getstatusoutput('gzip %s %s' % (force_switch, filename))

        if status != 0:
            
            if echoOnError:
                print 'Error: ' + status + ', ' +  output
            return ('error', output)

        else:
            return ('success', output)

    else:
        return ('error','file does %s not exist' % (filename))
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def set_file_mode(filename, user=['r'], group=None, other=None):

    permission_bits = 00000
    
    for current_bit in user:
        if current_bit == 's':
            permission_bits = permission_bits | stat.S_ISUID
        elif current_bit == 'r':
            permission_bits = permission_bits | stat.S_IRUSR
        elif current_bit == 'w':
            permission_bits = permission_bits | stat.S_IWUSR
        elif current_bit == 'x':
            permission_bits = permission_bits | stat.S_IXUSR

    if group != None:
        for current_bit in group:
            if current_bit == 's':
                permission_bits = permission_bits | stat.S_ISGID
            elif current_bit == 'r':
                permission_bits = permission_bits | stat.S_IRGRP
            elif current_bit == 'w':
                permission_bits = permission_bits | stat.S_IWGRP
            elif current_bit == 'x':
                permission_bits = permission_bits | stat.S_IXGRP
                
    if other != None:
        for current_bit in other:
            if current_bit == 'r':
                permission_bits = permission_bits | stat.S_IROTH
            elif current_bit == 'w':
                permission_bits = permission_bits | stat.S_IWOTH
            elif current_bit == 'x':
                permission_bits = permission_bits | stat.S_IXOTH
                
    os.chmod(filename, permission_bits)
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def dirWalker(arg, dirname, names):

    # if the current directory is not in exclusion list

    if dirname not in arg[1]:

        if dirname[:1] == '/':
            if string.find(dirname,'/',1) >= 0:
                parent_dir = dirname[:string.find(dirname,'/',1)]
                if parent_dir in arg[1]:
                    return
            
        if dirname[:2] == './':
            if string.find(dirname,'/',2) >= 0:
                parent_dir = dirname[:string.find(dirname,'/',2)]
                if parent_dir in arg[1]:
                    return

        for curfile in names:
                
            # if user just wants files not directories
            if arg[2]:

                if os.path.isfile(os.path.join(dirname,curfile)):

                    file_line = os.path.join(dirname[2:], curfile)

                    if arg[3]:
                        file_line = file_line + ' : file'

                    if arg[4]:
                        file_line = file_line + ' : ' + `os.path.getsize(os.path.join(dirname,curfile))`
                    
                    arg[0].append(file_line)
                    
            else:

                if os.path.isdir(os.path.join(dirname,curfile)) and \
                   os.path.join(dirname,curfile) not in arg[1]:
                    if arg[3]:
                        arg[0].append(os.path.join(dirname[2:], curfile) + ' : directory')
                    else:
                        arg[0].append(os.path.join(dirname[2:], curfile))

                elif os.path.isfile(os.path.join(dirname,curfile)):
                    
                    file_line = os.path.join(dirname[2:], curfile)
                    
                    if arg[3]:
                        file_line = file_line + ' : file'
                        
                    if arg[4]:
                        file_line = file_line + ' : ' + `os.path.getsize(os.path.join(dirname,curfile))`
                    
                    arg[0].append(file_line)
#---------------------------------------------------------------------
                    
                    
#---------------------------------------------------------------------
def walk_list_files(
    directory_name='.',
    list_only_files=0,
    exclude_list=[],
    include_file_type=0,
    include_file_size=0):

    list = []

    os.path.walk(directory_name, dirWalker, (list, exclude_list, list_only_files, include_file_type,include_file_size))
    
    list.sort()
    return list
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def disk_usage(directory_name):
    status, output = commands.getstatusoutput('du -b -c -s %s | grep total' % (directory_name))
    if status != 0:
        return ('error', -1)
    else:
        line_field = string.splitfields(output)
        return ('success', int(line_field[0]))
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def ppmToGif(ppmFilename,gifFilename):
    status, output = commands.getstatusoutput('ppmtogif %s > %s' % (ppmFilename,gifFilename))
    if status != 0:
        return ('error', output)
    else:
        return ('success', output)
#---------------------------------------------------------------------


#---------------------------------------------------------------------
def tempFile(dirPath='/usr/tmp', filePrefix='@'):

    if os.name == 'posix':
        _pid = os.getpid()
        tempfile.template = filePrefix + `_pid`
    elif os.name == 'nt':
        tempfile.template = '~' + `os.getpid()` + '-'
    elif os.name == 'mac':
        tempfile.template = 'Python-Tmp-'
    else:
        tempfile.template = 'tmp' # XXX might choose a better one
        
    tempfile.tempdir = dirPath
        
    return tempfile.mktemp()
#---------------------------------------------------------------------
