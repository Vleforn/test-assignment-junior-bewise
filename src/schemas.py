from pydantic import BaseModel, Field, ConfigDict

class BodyModel(BaseModel):
    question_num: int = Field(ge=0, lt=100)


class QuestionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    question: str
    answer: str
