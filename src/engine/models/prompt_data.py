from pydantic import BaseModel


class FrameExtractionPromptData(BaseModel):
    app_description: str
    your_role: str
    input_description: str
    output_description: str
    ocr_handling_guidance: str
    level_preamble: str
    level_1: str
    level_2: str
    level_3: str
    level_4: str
    example_return: str 

class FileCreationPromptData(BaseModel): 
    app_description: str 
    your_role: str
    reconstruction_guidelines: str
    attribution_requirements: str
    output_format: str 

