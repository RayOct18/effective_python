import subprocess


proc = subprocess.Popen(['sleep', '3'])
try:
    proc.communicate(timeout=1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())
