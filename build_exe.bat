@echo off
echo Building MarkItDown Desktop Application...
.\MarkItDown\Scripts\pyinstaller.exe MarkItDown.spec --noconfirm
echo.
echo Build finished! Executable is at dist\MarkItDown\MarkItDown.exe
pause
