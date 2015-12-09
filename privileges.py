import sys
import pwd
import grp
import os
import stat

class privileges:

	# python privilages.py backup find_path tofile
	# python privilages.py restore find_path fromfile
	file = ""
	path = ""
	method = ""

	def __init__(self):
		#print 'Argument List:', str(sys.argv)

		if len(sys.argv)==1:
			print "use help option: python privileges.py help"
			exit()
		
		if (sys.argv[1]=='help'):
			print "python privileges.py backup find_path tofile"
			print "python privileges.py restore find_path fromfile"
			exit()
		
		try:
			self.method = sys.argv[1]
		except:
			print "method needed"
			exit()

		try:
			self.file = sys.argv[3]
		except:
			self.file = None
			print "No file"
			exit()

		if (self.method=='backup' and self.file is not None):
			try:
				self.path = sys.argv[2]
			except:
				print "Path needed"
				exit()

			if self.path==".":
				self.path = os.getcwd()

			if self.path[-1]!="/":
				self.path +="/"

			self.makeBackup(self.path)

		if (self.method=='restore' and self.file is not None):
			try:
				self.path = sys.argv[2]
			except:
				print "Path needed"
				exit()

			if self.path[-1]!="/":
				self.path +="/"
			
			self.restoreBackup()

	def makeBackup(self, path):
		if open(self.file, 'a'):
			print "Saving possiblity correct..."
		else:
			print "Can not write to file"
			exit()

		with open(self.file, 'a') as file_:
			file_.write("#script used from " + os.path.abspath(sys.argv[0]) + "\n")
			file_.write("#script make backup for: " + path + "\n")

		self.move_on_tree(path)


	def restoreBackup(self):
		file = open(self.file,'r')
		for line in file:
			pieces = map(str.strip, line.split("|"))
			if len(pieces)==7:
				try:
					os.chown(pieces[6],int(pieces[1]),int(pieces[2]))
					print "chown: success " + self.path + pieces[6]
				except:
					print "chown: failed " + self.path + pieces[6]
				
				try:
					os.chmod(pieces[6],int(pieces[0]))
					print "chmod: success " + self.path + pieces[6]
				except:
					print "chmod: failed " + self.path + pieces[6]

	def move_on_tree(self, path):
		for root, dirs, files in os.walk(path):
			for name in files:
				self.make_line(os.path.join(root, name))
			for name in dirs:
				self.make_line(os.path.join(root, name))

	def permissions_to_unix_name(self, st):
		is_dir = 'd' if stat.S_ISDIR(st.st_mode) else '-'
		dic = {'7':'rwx', '6' :'rw-', '5' : 'r-x', '4':'r--', '0': '---'}
		perm = str(oct(st.st_mode)[-3:])
		return is_dir + ''.join(dic.get(x,x) for x in perm)

	def make_line(self, path_org):
		file = os.stat(path_org)
		string = str(file.st_mode) + " | "
		string += str(file.st_uid) + " | "
		string += str(file.st_gid) + " | "
		string += str(pwd.getpwuid(file.st_uid)[0]) + " | "
		string += str(grp.getgrgid(file.st_gid)[0]) + " | "
		string += self.permissions_to_unix_name(file) + " | "
		string += path_org.replace(self.path,"")
		print string
		self.save_to_file(string)

	def save_to_file(self, line):
		with open(self.file, 'a') as file_:
			file_.write(line+"\n")



priv = privileges()
