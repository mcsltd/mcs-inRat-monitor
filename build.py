import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    "--onefile",
    "--windowed",
    # "--console",
    "--name=inRat monitor",
    "--clean",
    "--icon=./resources/images/icon.ico",
])