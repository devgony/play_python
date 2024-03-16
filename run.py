from subprocess import call

def start():
    call("uvicorn play_python.main:app", shell=True)

def test():
    call("pytest -p no:warnings -v -s", shell=True)
