Build steps:

1. Create items for build process

```
pyinstaller --onefile main.py --collect-data graphics --collect-data font --collect-data sound --noconsole --icon icon.png
```

\*Note: For Windows users, if the build process encounters errors, go to your Windows Defender settings and allow the main.exe file created by PyInstaller. Windows Defender might prevent the build because it thinks your project is a virus.

\*Note: For Linux (Ubuntu) users, you need to install `binutils` if needed.

```
sudo apt install binutils -y
```

2. Add assets in .spec file

```
datas = [('graphics/*','graphics'),('font/*','font'),('sound/*','sound')]
```

3. Create executable file

```
pyinstaller main.spec
```
