#!/usr/bin/env python
from os import system
from time import sleep
from sys import argv, exit

def define_template():

	template = """<!DOCTYPE  html>
<html lang='en'>
	<head>
		<meta charset='utf-8'>
		<title>Template</title>
		<!-- Your code here -->
	</head>
	<body>
		<p>Template</p>
		<!-- Your code here -->
	</body>
</html>
"""
	return template

def create_file(t, f_name):
	
	try:
		with open(f'{f_name}.html', 'w+') as template_file:
			template_file.write(t)
	except:
		print("[x] Unable to write file!")
	finally:
		template_file.close() 

def get_args():

	if len(argv) is not 2:
		print("[x] Please provide a file name!")
		print(f"[!] Usage: html <file_name>")
		exit(0)
	else:
		return argv[1]
		pass

if __name__ == '__main__':

	create_file(define_template(), get_args())
