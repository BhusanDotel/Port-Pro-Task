from fastapi import FastAPI, HTTPException
from app.schemas import QueryRequest


app = FastAPI(title="PNCT Container Query API")

@app.get("/")
async def root():
    return {"status": "Healthy!"}


@app.post("/container/query")
async def query_container(req: QueryRequest):

    if not req.query or req.query.strip() == "":
        raise HTTPException(status_code=400, detail="query must be provided")
    try:
        print("Query received:", req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "data": "Query processed"}    