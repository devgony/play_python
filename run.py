from subprocess import call

def start():
    call("uvicorn play_python.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips '*' --reload", shell=True)

def test():
    call("pytest -p no:warnings -v -s", shell=True)
