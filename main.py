from fastapi import FastAPI, Depends, HTTPException, status, Header
from app.routes.todo_route import router as todo_router
from app.routes.label_route import router as label_router
from app.models.todo_model import Base
from app.database.database import engine, get_session


Base.metadata.create_all(engine)

app = FastAPI()


# movietronics_secret_api_key
def check_header(x_movitronics: str = Header(...)):
    if x_movitronics != "111":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )


def get_db():
    return get_session()


app.include_router(todo_router, dependencies=[Depends(check_header), Depends(get_db)])
app.include_router(label_router, dependencies=[Depends(check_header), Depends(get_db)])
