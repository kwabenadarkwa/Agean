# Agean 🐙

A software application that extracts source code from programming tutorial videos.

_Notes_

- Tesseract has to be installed and added to the path for this to work(I am going to end up using something else but for now)
- The thing you host the application on has to have ffmpeg installed in order for the splitting into frames to work

## Overall System Design

![System Design](./Images/System_Design.png)

## How to run

- Create a virtual environment using the command

```bash
python3 -m venv src/venv/bin/activate
```

- Install all dependencies using:

```bash
pip install -r requirements.txt
```

- Run the `main.py` file

```bash
python3 main.py
```

- In the case of ffmpeg, you will need to have already installed it on the maching to use it

## TODO

- [x] figure out how to extract other details from the video and then put it into an object
- [x] separate the video into frames
- [x] read SIFT documentation and use it to remove duplicate frames
- [x] extract source code from the frames
- [x] refactor codee to make use of the event pipeline to allow for easier testing
- [x] find test videos that contain only one file as the code
- [x] find test videos that contain only one file as the code but scrolling through the file from top to bottom
- [x] test refactored code
- [x] integrate telemetry into pipeline
- [x] add json file and refactor pipeline to test for particular video levels
- [x] verify that the batch pipeline works how it should
- [x] refactor the pipeline to use the youtube object instead of the link
  - would be needed when it comes to the gathering of data
- [x] refactor the main to use command line flags when starting to make it easier to test between different levels
- [x] make it such that we can use a particular pipeline based on level passed in the flag
- [x] add an event for dealing with the LLM
  - [x] add the LLM server information to an env file
  - [x] write an event that holds a prompt and then sends it to the LLM
  - [ ] add a script that starts the Ollama server how it should be done
- [ ] add an event that creates files after the LLM has finished/ also have another one if you don't use an LLM to parse(they could be the same mmom)
- [x] create a flag to specify which code extraction event to use
- [ ] fix the metrics measurements using the revised version of event_pipeline
- [ ] write an evaluate results event to the pipeline
- [ ] read literature on bounding box detection
- [ ] integrate bounding box detection
- [ ] use the literature to find the best method for frame content extraction

_Current Point_(Friday, July 18th 2025)

- I am done working on integrating the batch pipline fully.
- I also refactored the code to make it easier to read and understand and also test
- I added the use of command line flags to make sure that I can run the pipeline with a particular configuration when I want.

_Next Points_(Saturday, July 19th 2025)

- Finish the llm integration section(figure out exactly what prompt I'm going to use to get the best results)
- Consider including a file creation event after that section
- Add bounding box detection

_Current Point_(Saturday, July 19th 2025)

- The student tier that I have on Microsoft Azure has ended because I have overused my quota. I am going to have to pay for the premium version of deepseek.
