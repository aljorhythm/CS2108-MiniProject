import subprocess

def keyfindercli (src):
	return subprocess.check_output(['keyfinder-cli', src]).strip()