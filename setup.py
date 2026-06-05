import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"  

build_exe_options = {
    "packages": ["tkinter", "torch", "torch.nn", "torch.utils.data", "sklearn", "numpy", "datetime", "json", "re", "os", "sys", "load", "model", "modules", "gui", "main"],  
    "include_files": [] 
}

setup(
    name="ChatBot PyTorch Tkinter",
    version="1.0",
    description="ChatBot PyTorch avec interface Tkinter",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)

# commande : python setup.py build