# api.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from src.search_manager import SearchManager
from src.file_search_client import FileSearchClient
from src.document_processor import DocumentProcessor

app = FastAPI(title="RAG System API")

# Initialize components
client = FileSearchClient()
search_manager = SearchManager(client)
doc_processor = DocumentProcessor(client)

class QueryRequest(BaseModel):
    query: str
    store_name: str
    temperature: float = 0.0
    max_tokens: int = 1024

class QueryResponse(BaseModel):
    answer: str
    citations: List[dict]
    processing_time: float

@app.post("/api/search", response_model=QueryResponse)
async def search(request: QueryRequest):
    """Search and generate response from documents"""
    try:
        result = search_manager.search_and_generate(
            query=request.query,
            store_name=request.store_name,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return QueryResponse(
            answer=result.answer,
            citations=result.citations,
            processing_time=result.metadata.get('processing_time', 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile, store_name: str):
    """Upload a document to the store"""
    try:
        # Save temporary file and upload
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        result = doc_processor.upload_file(file_path, store_name)
        return {"success": True, "file_id": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stores")
async def list_stores():
    """List all available stores"""
    stores = client.list_stores()
    return {"stores": stores}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)