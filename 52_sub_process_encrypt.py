import os
import subprocess


def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7Sgioqrj*&^!$jPjaklsjd/.,)(!$'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)

for proc in procs:
    out, _ = proc.communicate()
    print(out, _)

def run_hash(input_stdin):
    return subprocess.Popen(
        ['openssl', 'dgst', '-whirlpool', '-binary'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)

encrypt_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None

for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out, _)
    assert proc.returncode == 0
