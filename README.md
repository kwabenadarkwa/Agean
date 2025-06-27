# Agean 🐙
A software application that extracts source code from programming tutorial videos.

*Notes*
- Tesseract has to be installed and added to the path for this to work(I am going to end up using something else but for now)
- The thing you host the application on has to have ffmped installed in order for the splitting into frames to work

## Overall System Design
![System Design](./Images/System_Design.png)

## How to run
- Create a virtual environment using the command

```bash
python3 -m venv <name_of_venv>
```

- Install all dependencies using: 

```bash
pip install -r requirements.txt
```

- Run the `main.py` file

```bash
python3 main.py
```

## TODO
- [x] figure out how to extract other details from the video and then put it into an object
- [x] separate the video into frames
- [x] read SIFT documentation and use it to remove duplicate frames
- [ ] extract source code from the frames
- [ ] find test videos that contain only one file as the code
- [ ] find test videos that contain only one file as the code but scrolling through the file from top to bottom




