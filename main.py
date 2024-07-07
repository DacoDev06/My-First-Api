from config.database import Session,engine,Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
from fastapi import FastAPI


app  = FastAPI(title="First API",version="0.0.1")
app.add_middleware(ErrorHandler)


Base.metadata.create_all(bind=engine)

@app.get('/',tags=["page"],response_class=HTMLResponse)
async def message():
    return """!
    """

#El orden en el que see incluye influye.
app.include_router(movie_router)
app.include_router(user_router)


    



    
