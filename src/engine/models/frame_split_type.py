class FrameSplitReturnType:
    """This class represents the return type of the `split_video_into_frames` function."""

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getstate__(self):
        return self.__dict__

    # TODO: returnType is the downloaderReturnType I think. it was erroring out so I remove it I will fix soon
    def __init__(self, returnType, frames_path):
        self.returnType = returnType
        self.frames_path = frames_path

    def __str__(self):
        return f"Title: {self.returnType.title 
        }\nTranscript: {self.returnType.transcript 
        }\nFrames Path: {self.frames_path}"
