from fastapi import APIRouter, Request , Depends, BackgroundTasks, Form
from typing import Annotated
from backend.utils.jwt import get_current_user

from backend.controller.v1 import user
from backend.controller.v1 import agent
from backend.models.ResponseModels import (
    FileUploadResponse, CandidateResponse, AnalysisResponse,
    DashboardStats, ProcessingStatus, DocumentProcessingRequest
)

from fastapi import UploadFile, File

router = APIRouter()


@router.get("/user-info")
async def user_data_wrapper(current_user: dict = Depends(get_current_user)):
    return await user.user_date(current_user)

@router.post("/file-upload")
async def file_upload_wrapper(
    current_user: dict = Depends(get_current_user),
    resume: UploadFile = File(...),
    offer: UploadFile = File(...),
    candidate_id: str = Form(...),
    placement_data: str = Form(...),
    placement_history: str = Form(...),
):
    return await agent.upload_files(
        current_user,
        candidate_id=candidate_id,
        resume=resume,
        offer=offer,
        placement_data=placement_data,
        placement_history=placement_history
    )
@router.get("/details")
async def file_upload_wrapper(current_user: dict = Depends(get_current_user)):
    return await agent.get_latest_candidate(current_user)

@router.post("/process")
async def file_process_wrapper(request_data: DocumentProcessingRequest, background_tasks: BackgroundTasks, current_user: dict=Depends(get_current_user)):
    return await agent.process_documents(current_user, request_data, background_tasks)

@router.get("/process/{session_id}/status", response_model=ProcessingStatus)
async def file_process_status_wrapper(session_id: str, current_user: dict=Depends(get_current_user)):
    return await agent.get_processing_status(current_user, session_id)
