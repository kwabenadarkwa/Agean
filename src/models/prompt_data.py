from pydantic import BaseModel


class PromptData(BaseModel):
    app_description: str
    your_role: str
    input_description: str
    output_description: str
    level_preamble: str
    level_1: str
    level_2: str
    level_3: str
    level_4: str
