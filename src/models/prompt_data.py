from pydantic import BaseModel


class FrameExtractionPromptData(BaseModel):
    app_description: str
    your_role: str
    input_description: str
    output_description: str
    level_preamble: str
    level_1: str
    level_2: str
    level_3: str
    level_4: str

class FileCreationPromptData(BaseModel): 
    app_description: str 
    your_role: str 

