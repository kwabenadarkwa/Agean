from download_type import DownloaderReturnType 


class BoundingBoxReturnType:
    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getstate__(self):
        return self.__dict__

    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        DownloaderReturnType: DownloaderReturnType,
        frames_path,
    ):
        self.DownloaderReturnType = DownloaderReturnType
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
        self.x2 = x2
        self.frames_path = frames_path

    def __str__(self):
        return f"x1: {self.x1}, y1: {self.y1}, x2: {self.x2}, y2: {self.y2}"
