from fastapi import HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import aiofiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from backend.utils.parsers import parse_date_safe
from beanie import PydanticObjectId

# agents
from backend.agents.offerAnalyzerAgent import run_offer_analyze_agent
from backend.agents.candidatePreferenceAgent import run_candidate_preference_agent
from backend.agents.acceptanceAgent import run_acceptance_agent
from backend.agents.upskillAgent import run_upskill_agent
from backend.agents.DashboardAgent import run_dashboard_agent

# models
from backend.models.Offer import Offer
from backend.models.Preference import Preference
from backend.models.CandidateReport import CandidateReport

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_files(
    user: dict,
    candidate_id: str = Form(...),
    resume: UploadFile = File(...),
    offer: UploadFile = File(...),
) -> JSONResponse:
    try:
        for uploaded_file, label in [(resume, "resume"), (offer, "offer")]:
            if not uploaded_file.filename.lower().endswith((".pdf", ".docx", ".doc")):
                raise HTTPException(status_code=400, detail=f"Only PDF and DOCX files are supported for {label}")

        def save_file(file: UploadFile, suffix: str) -> str:
            ext = os.path.splitext(file.filename)[1]
            file_id = f"{candidate_id}_{suffix}{ext}"
            file_path = os.path.join(UPLOAD_DIR, file_id)
            return file_path

        resume_path = save_file(resume, "resume")
        offer_path = save_file(offer, "offer")

        async with aiofiles.open(resume_path, 'wb') as f:
            await f.write(await resume.read())

        async with aiofiles.open(offer_path, 'wb') as f:
            await f.write(await offer.read())
            
        print(user)
            
        offer_response = run_offer_analyze_agent(offer_path)
        
        date_str = offer_response.get("joining_date")
        
        try:
            parsed_date = parse_date_safe(date_str)
        except Exception:
            parsed_date = None
        
        create_offer = Offer(
            userId=str(user["_id"]),
            bond_terms=offer_response.get("bond_terms" or None),
            job_title=offer_response.get("job_title"),
            salary=offer_response.get("salary"),
            location=offer_response.get("location"),
            joining_date=parsed_date
        )
        
        save_offer = await create_offer.save()
        
        candidate_response = run_candidate_preference_agent(resume_path)
        
        create_candidate_response = Preference(
            userId=str(user["_id"]),
            offerId=str(save_offer.id),
            preferred_location=candidate_response.get("preferred_location"),
            interests=candidate_response.get("interests"),
            skills=candidate_response.get("skills"),
            expected_ctc=candidate_response.get("expected_ctc" or None),
            career_goals=candidate_response.get("career_goals")
        )
        
        save_candidate_response = await create_candidate_response.save()
        
        acceptance = run_acceptance_agent(offer_analysis=offer_response, preference_alignment=candidate_response)
        
        print("==============", acceptance)
        
        save_offer.acceptance = int(acceptance["acceptance_likelihood"])
        save_offer.reason = acceptance["reasoning"]
        save_offer.confidence = int(acceptance["confidence"])
        
        await save_offer.save()
        
        upskill = run_upskill_agent(offer_analysis=offer_response, preference_alignment=candidate_response)
        
        save_offer.recommended_courses = upskill["recommended_courses"]
        save_offer.onboarding_resources = upskill["onboarding_resources"]
        save_offer.skill_gap_analysis = upskill["skill_gap_analysis"]
        await save_offer.save()

        dashboard_response = run_dashboard_agent(
            offer_analysis=offer_response, 
            preference_alignment=candidate_response, 
            acceptance_prediction=acceptance, 
            upskill_recommendations=upskill
            )
        
        store_candidate_report = CandidateReport(
            userId=str(user["_id"]),
            offerId=str(save_offer.id),
            preferenceId=str(save_candidate_response.id),
            report=dashboard_response
        )
        
        await store_candidate_report.save()

        return JSONResponse({
            "success": True,
            "message": "Files uploaded and analyzed successfully"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

async def get_candidate_analysis(user: dict):
    try:
        preference = await Preference.find(
            {"userId": PydanticObjectId(user["_id"])}
        ).sort("-created_at").first_or_none()

        if not preference:
            raise HTTPException(status_code=404, detail="Candidate preference not found.")

        offer = await Offer.find_one({"_id": preference.offerId})
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found.")
        
        final_report = await CandidateReport.find_one({"offerId": preference.offerId, "preferenceId": preference.id })

        response = {
            "candidate_id": "Candidate 1",
            "offer_analysis": {
                "position": offer.job_title,
                "salary": offer.salary.get("gross_annual") if offer.salary else None,
                "location": offer.location,
                "startDate": offer.joining_date.strftime("%Y-%m-%d") if offer.joining_date else None,
                "benefits": offer.bond_terms.split(",") if offer.bond_terms else []
            },
            "preference_alignment": {
                "preferredSalary": preference.expected_ctc,
                "locationPreference": preference.preferred_location,
                "keySkills": preference.skills,
                "alignmentScore": 85  
            },
            "acceptance_prediction": {
                "probability": offer.acceptance,
                "confidence": getattr(offer, "confidence", 90),
                "positiveFactors": ["Salary match", "Location aligned"],
                "riskFactors": ["Long bond period"] if offer.bond_terms else []
            },
            "upskill_recommendations": {
                "recommendations": [
                course if isinstance(course, str)
                else {"goal": course.get("goal", ""), "description": course.get("description", "")}
                for course in (offer.recommended_courses or [])
            ],
            "onboardingResource": [
                course if isinstance(course, str)
                else {"goal": course.get("goal", ""), "description": course.get("description", "")}
                for course in (offer.onboarding_resources or [])
            ]
            },
            "report": final_report.report,
            "status": "approved"
        }

        return JSONResponse({ "success": True, "data": jsonable_encoder(response) })

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

