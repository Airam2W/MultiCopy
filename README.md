# MultiCopy

MultiCopy is a desktop tool that you can use for copy multiple words, URLs or any texts what you need, and paste anything of them.
You can to configurete your favorite shortcut for MultiCopy, limited max of iteams to view (for a small interface), import or export yours clipboards created, and more.

---

## Why this project (MultiCopy) was created?

While I was copying large texts from some websites, images, titles, subtitles, a lot of thins interference me to copy everythins at once, I think "I want two Ctrl + V..." because is so tedious copy one for one.

And obviously, in the web exists a lot of professional clipboards, but I wanted to create a simple, easy to use and with characteristics that I consider useful for a clipboard.

---

## Good things about this project (MultiCopy)

- Can you copy a lot of texts (URLs, words, large texts) and have a list of its.
- Can you choice any word, URLs, text and paste it.
- MultiCopy have a special shortcut, you can change it if you want.
- Can configurate a limit of items to view in your list for paste and limit of items to copy.
- Can you Import/Export any clipboard that you want.
- Can view your current clipboard and edit any items that you want.
- Can save any configuration without loss it.

--- 

## Features of MultiCopy

- Easy to use.
- Simple interface.
- Useful functions better a native clipboard.
- Configuration persistence.

---

## Preview of MultiCopy

<img width="424" height="798" alt="image" src="https://github.com/user-attachments/assets/354c5673-cf20-4b09-a684-e98030350036" />
<img width="425" height="805" alt="image" src="https://github.com/user-attachments/assets/081d7ff1-fe58-43ff-b6f2-96ace2e05cbf" />
<img width="429" height="801" alt="image" src="https://github.com/user-attachments/assets/fbcbd791-f67e-46a2-b0f4-4170150bd838" />
<p align="center"><img src="https://github.com/user-attachments/assets/e90f3537-a2af-4300-bc2b-03eac9c4f4c8" alt="MultiCopy Demo 1" width="1919"/></p>
<p align="center"><img src="https://github.com/user-attachments/assets/5ee7cee9-7ca8-42d1-9887-b7a4453aa16e" alt="MultiCopy Demo - Copy text" width="1919"/></p>
<p align="center"><img src="https://github.com/user-attachments/assets/d6027792-1e9b-47b6-98e7-0c1d5aa56fd2" alt="MultiCopy Demo - Copy texts" width="1919"/></p>

---

## Installation

- Step 1. Download *MultiCopy.exe* located in the folder "dist"
- Step 2. Run *MultiCopy.exe* and Work with it!

> **If you want to package a python program (MultiCopy) into .exe:**  
> I recommend use this command for it:
```bash
pyinstaller --onefile --windowed --icon=utils/logo.ico main.py --add-data "utils/logo.ico;utils" --add-data "utils/config.json;utils" --add-data "utils/settings.ico;utils"
```

---

## Technologies

- Python (pyperclip, pynput, pyautogui, and others)

---

## Future Improvements

- Can copy Image, GIF, Videos, any file and other things besides text files.
- Improvement UI design.
- Improvement and add more functions.
