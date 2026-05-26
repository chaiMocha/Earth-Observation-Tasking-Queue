from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
import time
import logging

app = FastAPI(title="Earth Observation Tasking API")
logging.basicConfig(level=logging.INFO)

class TaskRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    priority: int = Field(default=1, ge=1, le=5, description="1 (Low) to 5 (High)")

def process_task(task_id: str, lat: float, lon: float, priority: int):
    logging.info(f"Task {task_id} queued. Target: ({lat}, {lon}) | Priority: {priority}")
    time.sleep(2)
    logging.info(f"Task {task_id} completed: Image captured.")

@app.post("/task", status_code=202)
async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
    task_id = f"task_{int(time.time())}"
    background_tasks.add_task(process_task, task_id, request.latitude, request.longitude, request.priority)
    return {"message": "Task accepted into queue", "task_id": task_id}