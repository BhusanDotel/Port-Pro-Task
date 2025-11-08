from fastapi import FastAPI, HTTPException
from app.agent import ContainerAgent
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
        agent = ContainerAgent() 
        result = await agent.process_query(req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "data": result}    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)