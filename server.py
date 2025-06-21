"""FastAPI server for LangManus Demo."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import logging
from src.main_app import LangManusAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LangManus Demo API",
    description="GitHub Repository Analyzer powered by LangManus",
    version="0.1.0"
)


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request model."""
    messages: List[ChatMessage]
    debug: bool = False


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LangManus Demo API",
        "version": "0.1.0",
        "description": "GitHub Repository Analyzer powered by LangManus"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint."""
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="No messages provided")
            
        # Get the last user message as the task
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user messages found")
            
        task = user_messages[-1].content
        
        # Create and run agent
        agent = LangManusAgent(task=task)
        result = agent.run()
        
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
            
        return {
            "report": result.get("report", ""),
            "chart_paths": result.get("chart_paths", []),
            "repo_url": result.get("repo_url", ""),
            "messages": result.get("messages", [])
        }
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint."""
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="No messages provided")
            
        # Get the last user message as the task
        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user messages found")
            
        task = user_messages[-1].content
        
        def generate_stream():
            try:
                agent = LangManusAgent(task=task)
                
                # Send initial status
                yield f"data: {json.dumps({'type': 'status', 'message': 'Starting analysis...', 'step': 'initializing'})}\n\n"
                
                # Stream workflow execution
                for state in agent.stream_run():
                    if isinstance(state, dict):
                        if state.get("error"):
                            yield f"data: {json.dumps({'type': 'error', 'message': state['error']})}\n\n"
                            break
                            
                        current_step = state.get("current_step", "unknown")
                        yield f"data: {json.dumps({'type': 'status', 'message': f'Processing step: {current_step}', 'step': current_step})}\n\n"
                        
                        # Send intermediate results
                        if state.get("repo_url"):
                            yield f"data: {json.dumps({'type': 'repo_found', 'repo_url': state['repo_url']})}\n\n"
                            
                        if state.get("chart_paths"):
                            yield f"data: {json.dumps({'type': 'charts_generated', 'chart_paths': state['chart_paths']})}\n\n"
                            
                        if state.get("report"):
                            yield f"data: {json.dumps({'type': 'report_ready', 'report': state['report']})}\n\n"
                            
                        # Send final result
                        if current_step == "complete":
                            final_result = {
                                'type': 'complete',
                                'report': state.get("report", ""),
                                'chart_paths': state.get("chart_paths", []),
                                'repo_url': state.get("repo_url", ""),
                                'messages': state.get("messages", [])
                            }
                            yield f"data: {json.dumps(final_result)}\n\n"
                            break
                
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                logger.error(f"Error in stream generation: {e}")
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        logger.error(f"Error in streaming chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008) 