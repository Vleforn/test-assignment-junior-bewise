from fastapi import FastAPI, Depends, status
from fastapi.responses import RedirectResponse
from database import Questions, get_session, init_db
from schemas import BodyModel, QuestionModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from external_api import request_questions, create_aiohttp_session

app = FastAPI(title="Questions")
app.add_event_handler("startup", init_db)
app.add_event_handler("startup", create_aiohttp_session)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url = "/docs")


@app.get("/questions", status_code=status.HTTP_200_OK, response_model=list[QuestionModel])
async def get_questions(session: Session = Depends(get_session)):
    stmt = select(Questions)
    questions = await session.execute(stmt)
    questions = questions.scalars().all()
    return questions


@app.post("/save", status_code=status.HTTP_201_CREATED, response_model=list[QuestionModel])
async def save_questions(body: BodyModel, session: Session = Depends(get_session)):
    num = body.question_num
    question_dict_list = await request_questions(num)
    question_models = []
    for question in question_dict_list:
        question_models.append(Questions(question=question["question"], answer=question["correct_answer"]))
    session.add_all(question_models)
    await session.commit()
    return question_models
