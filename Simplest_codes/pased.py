def insert_file():  # This fuction need to find the name of the file
	global file_name  # This variable is the name of the inputed file
	file_name = fd.askopenfilename()
	if file_name:
		detector = UniversalDetector()
		with open(file_name, 'rb') as fh:
			for line in fh:
				detector.feed(line)
				if detector.done:
					break
			detector.close()
		# ~ print(detector.result)
		if detector.result['encoding'] != 'UTF-8-SIG':
			file_name = ''
			btn_file['text'] = 'Выберите файл..'
			messagebox.showerror('Неверная кодировка файла','Неверная кодировка файла. Требуется UTF-8-SIG, обнаружена '+ detector.result['encoding'])
		else:
			lbl_file['bg'] = LBL_BG_CLEAN
			btn_file['text'] = file_name