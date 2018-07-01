# mirror_pmt.py

# Version 0.5
#
# mirror_pmt.py creates a backup of the main pmt server
#
# Scott Davis
#
#
# Version History
#
# 0.5 - pmt.backup file is automatically extracted and distributed
#	output is displayed in GUI
#	date of archive is displayed
#	auto ftp of most recent backup
#
# 0.4 - GUI
#
# 0.3 - version 0.3 allows for a file home.web.gz which contains /var/www/* from the
#	original host.  Also, html files are modified to make links point to files
#	on the mirror rather than the original host.
#
# 0.2 - version 0.2 backup up the web content, but not the documents directory.
#	use 'tar zcvf [db_name].web.gz --exclude documents -C /home/[db_name] .' to
#	create the data files stored in the web/ directory.
#
# 0.1 - version 0.1 backs up the existing databases and recreates them with the
#	*.db.dump.gz files created with dump_db.py


#-------------------------------------------------------------------------------
from Tkinter import *
import Pmw
import AppShell
import Callback
import os
import string
import time
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# All occurance of the old_host string will be replaced with new_host in html files
old_host='www.isrparc.org'
new_host='lanux'
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def get_db_list(output):
	output.insert(END,'Building list of databases to mirror.\n')
	#print 'Building list of databases to mirror.'
	db_list=[]
	dates=[]
	files=os.listdir('dump')
	for file in files:
		timestamp=time.strftime('%m/%d/%y %H:%M',time.localtime(os.stat('dump/'+file)[8]))
		parts=string.split(file,'.')
		dates.append(timestamp+' - '+parts[0])
		db_list.append(parts[0])
	return db_list,dates
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def backup_old_db(db_list,output):
	output.insert(END,'Backing up old databases.\n')
	#print 'Backing up old databases.'
	timestamp=time.strftime('%m_%d_%y',time.localtime(time.time()))

	for db_name in db_list:
		filename='backup/%s.%s.db.gz' % (db_name,timestamp)
		os.system('touch %s' % filename)
		os.system('pg_dump %s -U postgres | gzip > %s' % (db_name,filename))
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def create_new_db(db_list,output):
	output.insert(END,'Replacing old databases with new ones.\n')
	#print 'Replacing old databases with new ones.'
	for db_name in db_list:
		output.insert(END,'\tUpdating %s.\n' % db_name)
		#print "\tUpdating %s" % db_name
		os.system('dropdb %s -U postgres >> log.txt' % db_name)
		os.system('createdb %s -U postgres >> log.txt' % db_name)
		os.system('gunzip -f dump/%s.db.dump.gz >> log.txt 2>> err.txt' % db_name)
		os.system('psql %s -U postgres -f dump/%s.db.dump >> log.txt 2>> err.txt' % (db_name,db_name))
		os.system('gzip -f dump/%s.db.dump >> log.txt 2>> err.txt' % db_name)

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def mirror_db(db_list,output):
	backup_old_db(db_list,output)
	create_new_db(db_list,output)
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def get_web_list(output):
	output.insert(END,'Building list of websites to mirror.\n')
	#print 'Building list of websites to mirror.'
	web_list=[]
	dates=[]
	files=os.listdir('web')
	for file in files:
		timestamp=time.strftime('%m/%d/%y %H:%M',time.localtime(os.stat('web/'+file)[8]))
		parts=string.split(file,'.')
		dates.append(timestamp+' - '+parts[0])
		web_list.append(parts[0])
	return web_list,dates

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def backup_old_web(web_list,output):
	output.insert(END,'Backing up old websites.\n')
	#print 'Backing up old websites.'
	timestamp=time.strftime('%m_%d_%y',time.localtime(time.time()))


	for web_name in web_list:
		filename='backup/%s.%s.web.gz' % (web_name,timestamp)
		if web_name=='home':
			os.system('tar zcvf %s -C /var/www/ . >> log.txt 2>> err.txt' % (filename))
		else:
			os.system('tar zcvf %s --exclude documents -C /home/%s . >> log.txt 2>> err.txt' % (filename,web_name))
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def create_new_web(web_list,output):
	output.insert(END,'Replacing old web content.\n')
	#print 'Replacing old web content.'
	for web_name in web_list:
		output.insert(END,'\tUpdating %s.\n' % web_name)
		#print "\tUpdating %s" % web_name
		os.system('mkdir temp')
		os.system('tar zxvf web/%s.web.gz -C temp >> log.txt 2>>err.txt' % web_name)
		filelist=os.listdir('temp/html')
		for file in filelist:
			filename,ext=os.path.splitext(file)
			if ext=='.html':
				os.system('sed s/%s/%s/g temp/html/%s > temp/html/%s~' % (old_host,new_host,file,file))
				os.system('rename .html~ .html temp/html/*.html~')
		if web_name=='home':
			os.system('cp -rp temp/* /var/www/' )
		else:
			os.system('cp -rp temp/* /home/%s/' % web_name)
		os.system('rm -rf temp')

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def mirror_web(web_list,output):
	backup_old_web(web_list,output)
	create_new_web(web_list,output)
#-------------------------------------------------------------------------------


#===============================================================================
# MirrorApp class is the GUI
#===============================================================================
#
class MirrorApp(AppShell.AppShell):
#
#-------------------------------------------------------------------------------
#
	appname='PMT Mirror'
	frameWidth=500
	frameHeight=600
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def createMain(self):

		# Create text box for output
		self.output=Pmw.ScrolledText(self.interior())
		self.output.component('text').tag_configure('big',font=('Verdana',16))
		self.output.insert(END,'   Welcome to the PMT Mirroring System\n\n','big')

		file_windows=Frame(self.interior())

		# Create a list of available databases to backup
		db_frame=Frame(file_windows,borderwidth=2, relief=SUNKEN)
		db_label=Label(db_frame,text="Databases").pack(side=TOP)
		
		self.db_files=Pmw.ScrolledListBox(db_frame,
						  listbox_selectmode='extended',
						  listbox_exportselection=0,
						  items=get_db_list(self.output)[1])
		self.db_files.pack(side=TOP, fill='x')

		db_all=Button(db_frame, 
			      text='Select All', 
			      command=self.select_all_db_files)
		db_all.pack(side=TOP)

		db_refresh=Button(db_frame, 
				  text='Refresh', 
				  command=self.refresh_db_files)
		db_refresh.pack(side=TOP)

		# Create a list of available web content to backup
		web_frame=Frame(file_windows,borderwidth=2, relief=SUNKEN)
		web_label=Label(web_frame,text="Web Content").pack(side=TOP)

		self.web_files=Pmw.ScrolledListBox(web_frame,
						   listbox_selectmode='extended',
						   listbox_exportselection=0,
						   items=get_web_list(self.output)[1])
		self.web_files.pack(side=TOP, fill='x')

		web_all=Button(web_frame,
			       text='Select All',
			       command=self.select_all_web_files)
		web_all.pack(side=TOP)

		web_refresh=Button(web_frame,
				   text='Refresh',
				   command=self.refresh_web_files)
		web_refresh.pack(side=TOP)

		# Create the button that triggers the mirror
		mirror=Button(self.interior(),text='MIRROR',command=self.do_mirror)

		# Pack everything into the GUI
		db_frame.pack(side=LEFT, expand=1,fill='x',anchor=W)
		web_frame.pack(side=LEFT, expand=1, fill='x',anchor=E)
		file_windows.pack(side=TOP, expand=1, fill='both')
		mirror.pack(side=TOP)
		self.output.pack(side=TOP,expand=1, fill='both')
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def appInit(self):
		# Get the pmt.backup file from kenny if the local one is over 12 hours old
		backup_date=time.localtime(os.stat('pmt.backup')[8])
		now=time.localtime(time.time())
		#print "Backup_date: %s" % (time.strftime('%m/%d/%y %H:%M',time.localtime(os.stat('pmt.backup')[8])))
		#print "Now: %s" % (time.strftime('%m/%d/%y %H:%M',time.localtime(time.time())))
		if backup_date[:3]!=now[0:3]:
			print "Getting latest backup from kenny"
			os.system("su lliabraa -c 'sftp -b sftp.batch kenny'")
		else:
			print "Backup is up to date"

		# Uzip the current pmt.backup file and distribute its contents
		if os.path.exists('pmt.backup'):
			os.system('tar xf pmt.backup')
			os.system('mv *.web.gz web/')
			os.system('mv *.db.dump.gz dump/')
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def createInterface(self):
		self.createMain()
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def select_all_db_files(self):
		self.db_files.component('listbox').selection_set(0,END)
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def select_all_web_files(self):
		self.web_files.component('listbox').selection_set(0,END)
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def refresh_db_files(self):
		db_list=get_db_list(self.output)
		self.db_files.setlist(db_list[1])
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def refresh_web_files(self):
		web_list=get_web_list(self.output)
		self.web_files.setlist(web_list[1])
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
	def do_mirror(self):

		db_list=self.db_files.getcurselection()
		web_list=self.web_files.getcurselection()

		db_name_list=[]
		for db in db_list:
			db_name_list.append(string.split(db)[3])

		web_name_list=[]
		for web in web_list:
			web_name_list.append(string.split(web)[3])

		mirror_db(db_name_list,self.output)
		mirror_web(web_name_list,self.output)

		self.output.insert(END,'Done.\n\n')
		#print "Done"
#
#-------------------------------------------------------------------------------
#
#===============================================================================
# END MirrorApp CLASS
#===============================================================================


if __name__=='__main__':
	mirrorPMT=MirrorApp()
	mirrorPMT.run()
