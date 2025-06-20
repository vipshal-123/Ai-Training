from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
import os
import base64
import aiofiles
from datetime import datetime
import uuid
import asyncio
from contextlib import asynccontextmanager
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from backend.models import (
    UploadedFile, Candidate, AnalysisResult, 
)

from backend.models.AnalysisResult import (
    UpskillRecommendation, AcceptanceLikelihood, OfferAnalysis,
    CandidatePreference
)
from backend.models.Candidate import ( RiskLevel, CandidateStatus )
from backend.models.ResponseModels import (
    FileUploadResponse, CandidateResponse, AnalysisResponse,
    DashboardStats, ProcessingStatus
)
from backend.agents.DocumentProcessor import DocumentProcessor
from backend.models.UploadedFile import UploadedFile
from backend.models.AnalysisResult import AnalysisResult
from backend.models.Candidate import Candidate
from backend.models import ResponseModels
from beanie import PydanticObjectId
from backend.langgraph.runner import run_full_pipeline
from backend.utils.parsers import parse_gemini_response
from backend.utils.formatData import transform_results_for_frontend

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Processing status tracker
processing_status = {}

async def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Extract text from uploaded file"""
    try:
        if file_type.endswith('.pdf'):
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif file_type.endswith(('.docx', '.doc')):
            return DocumentProcessor.extract_text_from_docx(file_path)
        else:
            raise Exception("Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text: {str(e)}")


async def upload_files(
    user: dict,
    candidate_id: str = Form(...),
    resume: UploadFile = File(...),
    offer: UploadFile = File(...),
    placement_data: str = Form(...),
    placement_history: str = Form(...)
) -> JSONResponse:
    try:
        # Validate file types
        for uploaded_file, label in [(resume, "resume"), (offer, "offer")]:
            if not uploaded_file.filename.lower().endswith((".pdf", ".docx", ".doc")):
                raise HTTPException(status_code=400, detail=f"Only PDF and DOCX files are supported for {label}")

        # Helper to save file
        def save_file(file: UploadFile, suffix: str) -> str:
            ext = os.path.splitext(file.filename)[1]
            file_id = f"{candidate_id}_{suffix}{ext}"
            file_path = os.path.join(UPLOAD_DIR, file_id)
            return file_path

        # Save files to disk
        resume_path = save_file(resume, "resume")
        offer_path = save_file(offer, "offer")

        async with aiofiles.open(resume_path, 'wb') as f:
            await f.write(await resume.read())

        async with aiofiles.open(offer_path, 'wb') as f:
            await f.write(await offer.read())

        # === Run AI Pipeline ===
        results = run_full_pipeline(
            offer_path=offer_path,
            resume_path=resume_path,
            placement_data=placement_data,
            placement_history=placement_history,
        )
        
        result = transform_results_for_frontend(results)

        print("================", result)

        # Handle onboarding resource output
        onboarding = results.get("onboarding_resources", {})
        parsed_resources = parse_gemini_response(onboarding) if hasattr(onboarding, "text") or isinstance(onboarding, str) else onboarding

        # Create and store Candidate object
        candidate_record = Candidate(
            candidate_id="CANDIDATE",
            offer_analysis=result.get("offerAnalysis", {}),
            preference_alignment=result.get("candidatePreference", {}),
            acceptance_prediction={
                "probability": result.get("acceptanceLikelihood", {}).get("probability", 0),
                "confidence": result.get("acceptanceLikelihood", {}).get("confidence", 0),
                "riskFactors": result.get("acceptanceLikelihood", {}).get("riskFactors", []),
                "positiveFactors": result.get("acceptanceLikelihood", {}).get("positiveFactors", [])
            },
            upskill_recommendations=(
                {"recommendations": result.get("upskillRecommendations")}
                if isinstance(result.get("upskillRecommendations"), list)
                else result.get("upskillRecommendations", {})
            ),
            dashboard_summary={},
            status="pending"
        )

        await candidate_record.save()

        return JSONResponse({
            "success": True,
            "data": jsonable_encoder({"candidate_id": candidate_id}),
            "message": "Files uploaded and analyzed successfully"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/files")
async def get_latest_candidate(user: dict):
    try:
        latest_candidate = await Candidate.find_all().sort("-_id").limit(1).to_list()

        if not latest_candidate:
            raise HTTPException(status_code=404, detail="No candidate records found")

        candidate_data = jsonable_encoder(latest_candidate[0])

        return JSONResponse(content={
            "success": True,
            "data": candidate_data
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/api/files/{file_id}")
# async def delete_file(file_id: str):
#     """Delete an uploaded file"""
#     try:
#         # Get file info
#         file_doc = await db_manager.database.uploaded_files.find_one({"_id": ObjectId(file_id)})
#         if not file_doc:
#             raise HTTPException(status_code=404, detail="File not found")
        
#         # Delete physical file
#         if os.path.exists(file_doc["file_path"]):
#             os.remove(file_doc["file_path"])
        
#         # Delete from database
#         await db_manager.database.uploaded_files.delete_one({"_id": ObjectId(file_id)})
        
#         return {"message": "File deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

async def process_documents_background(session_id: str, resume_file_id: str, offer_file_id: str):
    """Background task to process documents"""
    try:
        print("=================", processing_status, "===================")

        processing_status[session_id] = {
            "status": "processing",
            "current_step": "Starting analysis",
            "progress": 10,
            "estimated_time": "2-3 minutes"
        }
        
        # Get file documents
        resume_doc = await UploadedFile.find_one({"_id": ObjectId(resume_file_id)})
        offer_doc = await UploadedFile.find_one({"_id": ObjectId(offer_file_id)})
        
        if not resume_doc or not offer_doc:
            raise Exception("Files not found")
        
        
        # Update status
        processing_status[session_id]["current_step"] = "Extracting document content"
        processing_status[session_id]["progress"] = 20
        print("===========1============")
        # Extract text from files
        resume_text = await extract_text_from_file(resume_doc.file_path, resume_doc.filename)
        offer_text = await extract_text_from_file(offer_doc.file_path, offer_doc.filename)

        print("=================2")
        # Update status
        processing_status[session_id]["current_step"] = "Running AI analysis"
        processing_status[session_id]["progress"] = 40
        
        print("=================3")
        
        # Process with AI agents
        analysis_result = predictor_workflow.process_documents(offer_text, resume_text)
        
        print("=================4")
        
        # Update status
        processing_status[session_id]["current_step"] = "Saving results"
        processing_status[session_id]["progress"] = 80
        
        # Extract candidate name from resume (simple extraction)
        candidate_name = "Unknown Candidate"  # You can implement name extraction logic
        
        # Create candidate record
        candidate = Candidate(
            name=candidate_name,
            position=analysis_result["offer_analysis"].get("position", "Unknown"),
            acceptance_probability=analysis_result["acceptance_likelihood"].get("probability", 50),
            status=CandidateStatus.PENDING,
            risk_level=RiskLevel.LOW if analysis_result["acceptance_likelihood"].get("probability", 50) > 70 else RiskLevel.HIGH,
            resume_file_id=str(resume_doc.id),
            offer_file_id=str(offer_doc.id)
        )
        
        candidate_result = await candidate.save()
        
        print("=============", candidate_result)
        
        candidate_id = str(candidate_result.id)
        
        print("==================", candidate_id)
        
        # Create analysis result record
        analysis_record = AnalysisResult(
            candidate_id=candidate_id,
            offer_analysis=OfferAnalysis(**analysis_result["offer_analysis"]),
            candidate_preference=CandidatePreference(**analysis_result["candidate_preference"]),
            acceptance_likelihood=AcceptanceLikelihood(**analysis_result["acceptance_likelihood"]),
            upskill_recommendations=[
                UpskillRecommendation(**rec) for rec in analysis_result["upskill_recommendations"]
            ]
        )
        
        analysis_result_db = await analysis_record.save()
        
        # Update candidate with analysis result ID
        await Candidate.update(
            {"_id": PydanticObjectId(candidate_id)},
            {"$set": {"analysis_result_id": PydanticObjectId(analysis_result_db.id)}}
        )
        
        # Mark files as processed
        await UploadedFile.update_all(
            {"_id": {"$in": [PydanticObjectId(resume_doc.id), PydanticObjectId(offer_doc.id)]}},
            {"$set": {"processed": True}}
        )
        
        # Update final status
        processing_status[session_id] = {
            "status": "completed",
            "current_step": "Analysis completed",
            "progress": 100,
            "estimated_time": "0 minutes",
            "candidate_id": str(candidate_id)
        }
        
    except Exception as e:
        processing_status[session_id] = {
            "status": "failed",
            "current_step": f"Error: {str(e)}",
            "progress": 0,
            "estimated_time": "0 minutes"
        }

# @app.post("/api/process")
async def process_documents(user, request_data, background_tasks):
    """Start document processing"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        resume_file_id = request_data.resume_file_id
        offer_file_id = request_data.offer_file_id
        
        # Validate file IDs
        resume_doc = await UploadedFile.find_one({"_id": ObjectId(resume_file_id)})
        offer_doc = await UploadedFile.find_one({"_id": ObjectId(offer_file_id)})
        
        if not resume_doc or not offer_doc:
            raise HTTPException(status_code=404, detail="One or both files not found")
        
        # Start background processing
        background_tasks.add_task(
            process_documents_background,
            session_id,
            resume_file_id,
            offer_file_id
        )
        
        return {
            "session_id": session_id,
            "message": "Processing started",
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/process/{session_id}/status", response_model=ProcessingStatus)
async def get_processing_status(user, session_id: str):
    """Get processing status"""
    if session_id not in processing_status:
        raise HTTPException(status_code=404, detail="Session not found")
    
    status = processing_status[session_id]
    return ProcessingStatus(
        status=status["status"],
        current_step=status["current_step"],
        progress=status["progress"],
        estimated_time=status["estimated_time"]
    )

# @app.get("/api/candidates", response_model=List[CandidateResponse])
# async def get_candidates():
#     """Get all candidates"""
#     try:
#         candidates = []
#         async for candidate_doc in db_manager.database.candidates.find():
#             candidates.append(CandidateResponse(
#                 id=str(candidate_doc["_id"]),
#                 name=candidate_doc["name"],
#                 position=candidate_doc["position"],
#                 acceptance_probability=candidate_doc["acceptance_probability"],
#                 status=candidate_doc["status"],
#                 risk_level=candidate_doc["risk_level"],
#                 upload_date=candidate_doc["upload_date"].isoformat()
#             ))
#         return candidates
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/candidates/{candidate_id}", response_model=CandidateResponse)
# async def get_candidate(candidate_id: str):
#     """Get specific candidate"""
#     try:
#         candidate_doc = await db_manager.database.candidates.find_one({"_id": ObjectId(candidate_id)})
#         if not candidate_doc:
#             raise HTTPException(status_code=404, detail="Candidate not found")
        
#         return CandidateResponse(
#             id=str(candidate_doc["_id"]),
#             name=candidate_doc["name"],
#             position=candidate_doc["position"],
#             acceptance_probability=candidate_doc["acceptance_probability"],
#             status=candidate_doc["status"],
#             risk_level=candidate_doc["risk_level"],
#             upload_date=candidate_doc["upload_date"].isoformat()
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/candidates/{candidate_id}/analysis", response_model=AnalysisResponse)
# async def get_candidate_analysis(candidate_id: str):
#     """Get candidate analysis results"""
#     try:
#         candidate_doc = await db_manager.database.candidates.find_one({"_id": ObjectId(candidate_id)})
#         if not candidate_doc:
#             raise HTTPException(status_code=404, detail="Candidate not found")
        
#         if not candidate_doc.get("analysis_result_id"):
#             raise HTTPException(status_code=404, detail="Analysis not found")
        
#         analysis_doc = await db_manager.database.analysis_results.find_one(
#             {"_id": candidate_doc["analysis_result_id"]}
#         )
        
#         if not analysis_doc:
#             raise HTTPException(status_code=404, detail="Analysis results not found")
        
#         return AnalysisResponse(
#             offer_analysis=analysis_doc["offer_analysis"],
#             candidate_preference=analysis_doc["candidate_preference"],
#             acceptance_likelihood=analysis_doc["acceptance_likelihood"],
#             upskill_recommendations=analysis_doc["upskill_recommendations"]
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.put("/api/candidates/{candidate_id}/status")
# async def update_candidate_status(candidate_id: str, status: CandidateStatus):
#     """Update candidate status"""
#     try:
#         result = await db_manager.database.candidates.update_one(
#             {"_id": ObjectId(candidate_id)},
#             {"$set": {"status": status.value, "updated_at": datetime.utcnow()}}
#         )
        
#         if result.matched_count == 0:
#             raise HTTPException(status_code=404, detail="Candidate not found")
        
#         return {"message": "Status updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/api/candidates/{candidate_id}")
# async def delete_candidate(candidate_id: str):
#     """Delete a candidate and associated data"""
#     try:
#         candidate_doc = await db_manager.database.candidates.find_one({"_id": ObjectId(candidate_id)})
#         if not candidate_doc:
#             raise HTTPException(status_code=404, detail="Candidate not found")
        
#         # Delete analysis results
#         if candidate_doc.get("analysis_result_id"):
#             await db_manager.database.analysis_results.delete_one(
#                 {"_id": candidate_doc["analysis_result_id"]}
#             )
        
#         # Delete candidate
#         await db_manager.database.candidates.delete_one({"_id": ObjectId(candidate_id)})
        
#         return {"message": "Candidate deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/dashboard/stats", response_model=DashboardStats)
# async def get_dashboard_stats():
#     """Get dashboard statistics"""
#     try:
#         # Total candidates
#         total_candidates = await db_manager.database.candidates.count_documents({})
        
#         # Average acceptance rate
#         pipeline = [
#             {"$group": {"_id": None, "avg_acceptance": {"$avg": "$acceptance_probability"}}}
#         ]
#         avg_result = await db_manager.database.candidates.aggregate(pipeline).to_list(1)
#         avg_acceptance_rate = avg_result[0]["avg_acceptance"] if avg_result else 0
        
#         # High confidence count (>80% acceptance probability)
#         high_confidence_count = await db_manager.database.candidates.count_documents(
#             {"acceptance_probability": {"$gte": 80}}
#         )
        
#         # High risk count
#         high_risk_count = await db_manager.database.candidates.count_documents(
#             {"risk_level": "high"}
#         )
        
#         return DashboardStats(
#             total_candidates=total_candidates,
#             avg_acceptance_rate=round(avg_acceptance_rate, 2),
#             high_confidence_count=high_confidence_count,
#             high_risk_count=high_risk_count
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/candidates/{candidate_id}/upskill-recommendations")
# async def get_upskill_recommendations(candidate_id: str):
#     """Get upskilling recommendations for a candidate"""
#     try:
#         candidate_doc = await db_manager.database.candidates.find_one({"_id": ObjectId(candidate_id)})
#         if not candidate_doc:
#             raise HTTPException(status_code=404, detail="Candidate not found")
        
#         if not candidate_doc.get("analysis_result_id"):
#             raise HTTPException(status_code=404, detail="Analysis not found")
        
#         analysis_doc = await db_manager.database.analysis_results.find_one(
#             {"_id": candidate_doc["analysis_result_id"]}
#         )
        
#         if not analysis_doc:
#             raise HTTPException(status_code=404, detail="Analysis results not found")
        
#         return analysis_doc["upskill_recommendations"]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/health")
# async def health_check():
#     """Health check endpoint"""
#     try:
#         # Test database connection
#         await db_manager.client.admin.command('ismaster')
#         return {
#             "status": "healthy",
#             "timestamp": datetime.utcnow().isoformat(),
#             "database": "connected"
#         }
#     except Exception as e:
#         return {
#             "status": "unhealthy",
#             "timestamp": datetime.utcnow().isoformat(),
#             "database": "disconnected",
#             "error": str(e)
#         }

# # Error handlers
# @app.exception_handler(ValueError)
# async def value_error_handler(request, exc):
#     return JSONResponse(
#         status_code=400,
#         content={"detail": str(exc)}
#     )

# @app.exception_handler(Exception)
# async def general_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "Internal server error"}
#     )
