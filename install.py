import os, sys, shutil, subprocess

def getLocation():
  if os.name == "nt":
    return os.path.join("\\".join(sys.executable.split("\\")[:-1]), "Scripts")
  else:
    return "/".join(sys.executable.split("/")[:-1])

def log(text):
  print("log: " + text)

def install():
  path = getLocation()
  if os.name == "nt":
    log("non-posix operating system detected")
    log("moving executable...")
    shutil.move("installer\\stamp.bat", os.path.join(path, "pom.bat"))
    log("done")
  else:
    log("posix operating system detected")
    log("moving executable...")
    shutil.move("installer/stamp.sh", os.path.join(path, "pom"))
    log("done")
    log("setting permissions...")
    os.system("chmod 777 " + os.path.join(path, "pom"))
    log("done")
  log("cleaning up...")
  shutil.rmtree("stamp")
  shutil.rmtree("installer")
  os.remove("install.py")
  os.remove("setup.py")
  log("done (enter to finish installer)")
  input()

print("""   ___________      __  _______     ____           __        ____         
  / ___/_  __/___ _/  |/  / __ \   /  _/___  _____/ /_____ _/ / /__  _____
  \__ \ / / / __ `/ /|_/ / /_/ /   / // __ \/ ___/ __/ __ `/ / / _ \/ ___/
 ___/ // / / /_/ / /  / / ____/  _/ // / / (__  ) /_/ /_/ / / /  __/ /    
/____//_/  \__,_/_/  /_/_/      /___/_/ /_/____/\__/\__,_/_/_/\___/_/     """)

log("starting module install...")

try:
  with open(".pip_output", "w") as pipOut:
    outputv = subprocess.run([sys.executable, "-m", "pip", "install", "."], stdout=pipOut, stderr=pipOut)
except KeyboardInterrupt:
  os.remove(".pip_output")
  print("")
  log("pip install failed, keyboard interrupt")
  sys.exit()

if str(outputv.returncode) == "0":
  log("done")
else:
  log("pip install failed, see '.pip_output'")
  sys.exit()

log("cleaning up...")
os.remove(".pip_output")
log("done\n")

log("starting STaMP install...")
try:
  install()
except PermissionError:
  log("failed to create executable, please run command with 'sudo'")