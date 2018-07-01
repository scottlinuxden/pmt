# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Lane LiaBraaten
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#
import os
import os.path
import sys
import commands
import os_utils
import glob
import string

"""Date keywords for no_later_than_date can include
Now, 1 hour ago, and date itself"""

ignore_file_list = glob.glob('*.pyc') + \
                   glob.glob('*~') + \
                   glob.glob('#*#') + \
                   glob.glob('*.o') + \
                   glob.glob('core') + \
                   glob.glob('*.tgz') + \
                   glob.glob('*.tar') + \
                   glob.glob('*.tar.gz') + \
                   glob.glob('*.zip')

#--------------------------------------------------------------------------
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
					
		return ('success', output)
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def process_command_output(output,eol='\012'):
    """ eol should be \012 for Unix or \015\012 for windows"""

    command_output = []
    output_line = 0
    lines = string.splitfields(output, eol)
    while output_line < len(lines):
        if string.strip(lines[output_line]) != '':
            command_output.append(string.splitfields(lines[output_line]))
        output_line = output_line + 1
    return command_output
#--------------------------------------------------------------------------
                             

#--------------------------------------------------------------------------
def get_response(question,example,default=None,required=0):
    while 1:
        print '%s? (Example: %s) [Default: %s]: ' % (question,example,default),
        answer = sys.stdin.readline()[:-1]
        if default == None:
            if string.strip(answer) != '':
                 return answer
            else:
                if required:
                    'You must supply a response'
                else:
                    return ''
        else:
            if string.strip(answer) != '':
                return answer
            else:
                return default
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def get_yes_no_response(question):
    while 1:
        print "%s? [Y/N]: " % (question),
        answer = sys.stdin.readline()[:-1]
        if answer in ['Y','y','N','n']:
            if answer in ['Y', 'y']:
                return 'Y'
            else:
                return 'N'
        else:
            print 'Invalid reply'
#--------------------------------------------------------------------------
    

#--------------------------------------------------------------------------
def confirm_delete(filename):
    while 1:
        print "Are you sure you want to delete %s?" % (filename)
        answer = sys.stdin.readline()
        if answer in ['Y','y','N','n']:
            if answer in ['Y', 'y']:
                return 1
            else:
                return 0
        else:
            print 'Invalid reply'
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def cvs_get_root(echo=0):
    status, setting = os_utils.getenv('CVSROOT')
    if status != 'success':
        if echo:
            print 'error: CVSROOT is not defined'
        return ('error', 'CVSROOT is not defined')
    else:
        return (status, setting)
#--------------------------------------------------------------------------
    

#--------------------------------------------------------------------------
def cvs_root_set(echo=0):
    status, output = cvs_get_root(echo=1)
    if status != 'success':
        return ('error','CVSROOT is not defined')
    else:
        return ('success','CVSROOT is defined')
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def cvs_remove(filename,echo=0,recursive=1):

    status, output = cvs_root_set(echo=echo)

    if status != 'success':
        return (status, output)

    options = ' '
    if not recursive:
        options = '-l'
        
    if os.path.isfile(filename):
        if get_yes_no_response('Are you sure you want to remove the file %s' % (filename)) == 'Y':

            command_status, output = commands.getstatusoutput('cvs remove -f %s %s' % (options,filename))

            if command_status != 0:
                return ('error', 'CVS could not remove the file %s' % (filename))

            return ('success', output)

        else:
            return ('success',
		    'User cancelled removal of the file %s'  % (filename))

    elif os.path.isdir(filename):

        if get_yes_no_response('Are you sure you want to remove the directory %s and all files and subdirectories in that directory' % (filename)) == 'Y':

            # remove the directory and all subdirectories
            command_status, output = commands.getstatusoutput('cvs remove -f %s %s' % (options,filename))

            if command_status != 0:
                return ('error', 'CVS could not remove the directory %s' % (filename))
            
            return ('success', output)

        else:
            return ('success',
		    'User cancelled removal of the directory %s'  % (filename))
#--------------------------------------------------------------------------
                    

#--------------------------------------------------------------------------
def cvs_commit(echo=0,comment=''):

    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    command_status, output = commands.getstatusoutput("cvs commit -m '%s'" % (comment))

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error',output)
        return ('error',output)

    return ('success', output)
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def cvs_add(filename,echo=0):
    """ cvs add requires the current directory to be the directory
    where the file is to add"""

    # get the current working directory
    current_directory = os.getcwd()
    
    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    # if current working directory is not the directory where file is at
    if current_directory != os.path.abspath(os.path.dirname(filename)):
        # change working to directory to where file is at
        os.chdir(os.path.abspath(os.path.dirname(filename)))
                
    command_status, output = commands.getstatusoutput('cvs add %s' % (os.path.basename(filename)))

    os.chdir(current_directory)

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error',output)
        return ('error',output)
    
    return ('success', output)
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def cvs_init(repository=None,echo=0):
    """ Initialize a directory tree that will support CVS
    typically repository would be /cvsroot.
    arguments:
    repository must be the complete file path to the new cvs repository"""
    
    if repository == None:
        while 1:
            print "Enter name of repository to create? ",
            repository = sys.stdin.readline()[:-1]
            if string.strip(repository) != '':
                break

    if not os.path.exists(repository):
        print 'Destination directory: %s does not exist.' % (repository)
        if get_yes_no_response('Do you want to create the directory') == 'Y':
            os.makedirs(name=repository, mode=0755)
        else:
            if echo:
                print 'User cancelled init'
            return ('error', 'User cancelled init')
        
    command_status, output = commands.getstatusoutput('cvs -d %s init' % (repository))

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error',output)
        return ('error',output)
    
    return ('success', output)
#--------------------------------------------------------------------------
	

#--------------------------------------------------------------------------
def cvs_import(repository,
	       distribution_name,
	       version, release,
	       vendor_name='ISR',
	       comment='Initial Import',
	       ignore_files=ignore_file_list,
	       echo=0):
    """ Imports source files in current working directory to the CVS repository
    arguments:
    repository is the directory under CVS root directory to put the files that
    will be imported
    vendor_name is name of company"""

    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    options = ' '
    if ignore_files != None:
        file_list_to_ignore = ' '
        for i in ignore_files:
            file_list_to_ignore = file_list_to_ignore + i + ' '
        options = "-I '%s'" % file_list_to_ignore
        
    command_status, output = commands.getstatusoutput("cvs import -d %s -m '%s' %s %s_%s %s_%s_%s" % (options,comment,repository,string.upper(vendor_name),string.upper(distribution_name),string.upper(distribution_name),version,release))
        
    if command_status != 0:
        if echo:
            print '%s: %s' % ('error', output)
        return ('error',output)
    
    return ('success', output)
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def cvs_export(distribution_name,
	       destination_directory,
	       no_later_than_date,
	       tag,echo=1, module_path=None):

    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    if not os.path.exists(destination_directory):
        print 'Destination directory: %s does not exist.' % (destination_directory)
        if get_yes_no_response('Do you want to create the directory') == 'Y':
            os.makedirs(name=destination_directory, mode=0755)
        else:
            if echo:
                print '%s: %s' % ('error','export cancelled by user')
            return ('error','export cancelled by user')

    options = ' '
    if no_later_than_date != None:
        options = options + "-D '%s'" % (no_later_than_date)
    elif tag != None:
        options = options + "-r '%s'" % (tag)

    options = options + " -d '%s' " % (distribution_name)

    os.chdir(destination_directory)

    cmd='cvs export %s %s' % (options,module_path)
    #print "<BR>%s<BR>" % cmd
    #print "<BR>%s<BR>" % os.getcwd()
    command_status, output = commands.getstatusoutput(cmd)

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error',output)
        return ('error', output)
    
    return ('success', output)
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def cvs_tag(distribution_name,
	    major_version,
	    minor_version,
	    tag_what='repository',echo=0):
    """ distribution_name such as save
    major_version = integer
    minor_version = integer
    tag_what = (repository or working_directory) """

    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    label = "%s-%s-%s" % (string.lower(distribution_name),
			  major_version,
			  minor_version)
    
    options = ' '
    if tag_what == 'repository':
        options = options + "-rtag '%s'" % (label)
    elif tag_what == 'working_directory':
        options = options + "-tag '%s'" % (label)
        
    command_status, output = commands.getstatusoutput('cvs %s %s' % (options,distribution_name))

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error',output)

    return ('success', output)
#--------------------------------------------------------------------------
    

#--------------------------------------------------------------------------
def cvs_export_encapsulate_distribution(distribution_name,
					encapsulation_method,
					encapsulated_file_location,
					no_later_than_date,
					tag,echo, module_path=None):

    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output, None)

    if not os.path.exists(encapsulated_file_location):
        os.mkdir(encapsulated_file_location)
    
    status, output = cvs_export(distribution_name,
				encapsulated_file_location,
				no_later_than_date,
				tag,echo,module_path)
  
    #status, output = cvs_export(distribution_name,
    #                            encapsulated_file_location,
    #                            no_later_than_date,tag,echo)
  
    if status != 'success':
        if echo:
            print '%s: %s' % (status,output)

        return (status, output, None)

    os.chdir(encapsulated_file_location)


    if encapsulation_method == 'tar':
        status, output = commands.getstatusoutput('pwd')
        status, output = tar_create('../' + distribution_name + '.tar', '*', 1)
        if status != 'success':
            if echo:
                print '%s: %s' % (status,output)
            return (status, output, None)
    
        tar_ball_contents = output

        status, output = os_utils.gzip('../' + distribution_name + '.tar',1,0)
        if status != 'success':
            if echo:
                print '%s: %s' % (status,output)
            return (status, output, None)

    elif encapsulation_method == 'zip':
        pass

    os_utils.super_remove(encapsulated_file_location)
        
    return ('success','export distribution successful', tar_ball_contents)
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
def file_in_cvs(filename,echo=0):
    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    command_status, output = commands.getstatusoutput('cvs status %s' % filename)

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error',output)
        return 0

    result_lines = process_command_output(output)

    if (result_lines[0][0][:3] == '===') or \
       (len(result_lines) > 1 and result_lines[0][2] == 'Examining' and result_lines[1][0][:3] == '==='):
        return 1
    else:
        return 0
#--------------------------------------------------------------------------
    

#--------------------------------------------------------------------------
def cvs_checkout(module_name,destination_directory,tag=None,echo=0):

    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    if not os.path.exists(destination_directory):
        print 'Destination directory: %s does not exist.' % (destination_directory)

        if get_yes_no_response('Do you want to create the directory') == 'Y':
            os.makedirs(name=destination_directory, mode=0755)
        else:
            if echo:
                print '%s: %s' % ('error','User cancelled checkout since directory does not exist')
            return ('error', 'User cancelled checkout since directory does not exist')
            
    os.chdir(destination_directory)

    options = ' '

    if tag != None:
        options = options + "-r '%s'" % (tag)

    command_status, output = commands.getstatusoutput('cvs checkout -P %s %s' % (options,module_name))

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error', output)
        return ('error', output)

    return ('success', output)
#--------------------------------------------------------------------------
                    

#--------------------------------------------------------------------------
def cvs_release(working_directory,echo=0,delete=0):

    status, output = cvs_root_set(echo=echo)
    if status != 'success':
        return (status, output)

    os.chdir(os.path.dirname(working_directory))
    
    options = ' '
    if delete:
        options = '-d'
        
    command_status, output = commands.getstatusoutput('cvs release %s %s' % (options,os.path.basename(working_directory)))

    if command_status != 0:
        if echo:
            print '%s: %s' % ('error',output)
        return ('error',output)

    return ('success', output)
#--------------------------------------------------------------------------

