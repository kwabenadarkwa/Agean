# Agean 🐙

A software application that extracts source code from programming tutorial videos.

It has three different parts:
- The engine which is the core of how everything works that is built with the event pipeline 
- The server which serves the engine as a REST API that can be used with whatever frontend you want.
- The browser extension which uses the server to extract code from whatever youtube video you're currently watching.

_Notes_

- Tesseract has to be installed and added to the path for this to work(I am going to end up using something else but for now)
- The thing you host the application on has to have ffmpeg installed in order for the splitting into frames to work
- You might have to install the _event_pipeline_ package from the git repository and then install it from source for it to work

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
- [x] create a flag to specify which code extraction event to use
- [x] read literature on bounding box detection
- [x] fix the metrics measurements using the revised version of event_pipeline
- [x] create a standard json file to measure the results against
- [x] integrate bounding box detection
- [x] use the literature to find the best method for frame content extraction(replace with what you currently have)

==Final countdown tomorrow==

- [x] add an event that creates files after the LLM has finished/ also have another one if you don't use an LLM to parse(they could be the same mmom)
- [ ] package tool as a browser extension(might need docker)
- [ ] continue the implementation part of writing the report
- [ ] maybe it might be a sensible step to figure out which bounding box contains the code elements. # so maybe instead of actually finding the bouding box. we send the texts object that is extracted. we comb through the texts object # to find which of the descriptions actually contains code. and then remove the ones that don't. that could be a step after this point(using the google ocr thing of course.). this couuld be the final form to reduce the amount of time that things take. nice

## TESTING

- [x] Test rule based filtering in the entire pipeline as a whole
- [ ] Write a test condition after the LLM is done parsing everything

## BUGS

- [ ] add a thing that checks the input size of the data to the LLM and stop it in that case(or iterate and then split the thing into mutiple prompts or something)

_Remaining Points_

- create a standard json file to measure the results against
- finish the bounding box detection
- decide which method has higher accuracy
- reconstruct the file structure for level 1 and level 2 and level 3
- for level 4 train model to determine file that's opened first and assign code snippet to opened file
- create the files that are detected in the file structure for level 4
- use image super resolution to increase the resolution of the images(maybe that's going to increase the accuracy of the results)

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
- I've been able to add the LLM to the pipeline and now I'm paying some money to use deepseek.

_Next Points_(Sunday, July 20th 2025)

- Fix the issues that are occurring with the metrics feature
- include tracking of the metrics per event in the pipeline

_Current Point_(Sunday, July 20th 2025)

- fixed the metrics issues so now the metrics show and you get a json file with them.
- they show how long each event takes in the pipeline but there's the problem with the batch pipeline not being tracked properly

_Next Points_(Monday, July 21st 2025)

- do research on the bounding box detection
- figure out how to use it based on the literature

_Current Point_(Monday, July 20th 2025)

- Read through PSC2CODE code and find where they're doing the bounding box detection
- After that, use the code and the data they have to train a model that you can use

_Current Point_(Monday, July 28th 2025)

- I've started encoding the data into the json file and I've done just one.
- I have 19 more to go.
- it's taking more time than I thought it would take

_Current Point_(Tuesday, July 20th 2025)

- continue the encoding and try and finish it
