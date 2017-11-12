import transposer
import os
from multiprocessing import Process, Manager, Lock
import time

mutex = Lock()

def task (path, outdir, filename, i, result ):
	src = "%s/%s" % (path, filename)
	out = "".join([outdir, "/", os.path.splitext(os.path.basename(src))[0], "_transposed_", str(i), ".wav"])

	if not os.path.exists(out):
		transposer.transpose(src, out, i)

	mutex.acquire()
	if filename not in result:
		result[filename] = {}
	if "original-key" not in result[filename]:
		o = result[filename]
		o['original-key'] = transposer.findkey(src)
		result[filename] = o
	mutex.release()

	mutex.acquire()
	o = result[filename]
	o[i] = transposer.findkey(out)
	result[filename] = o
	mutex.release()

def runtest ():
	path = "./src/songs"
	outdir = "./src/transposed"
	manager = Manager()
	pids = []

	presult = manager.dict()
	result = {}

	for filename in os.listdir(path):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			presult[filename] = {}
			o = presult[filename]
			o['original-key'] = ""


	for filename in os.listdir(path):
		if filename.endswith(".wav") or filename.endswith("mp3"):
			for i in range (1,13):
				pid = Process(target=task, args=(path, outdir, filename, i, presult, ))
				pids.append(pid)
				pid.start()
			

	for pid in pids:
		pid.join()

	for filename in presult.keys():
		print " ".join(["Filename:", filename])
		print " ".join(["Original Key:", presult[filename]['original-key']])
		for i in presult[filename]:
			if i == "original-key": 
				continue;
			print " ".join(["\t", "Steps:", str(i), "-", "Key:", presult[filename][i]])
			print ""


if __name__ == '__main__':
	runtest()