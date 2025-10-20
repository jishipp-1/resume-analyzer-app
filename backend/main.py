from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Auth functions (relative import)
from .auth import hash_password, verify_password, create_access_token

# Database (relative import)
from .database import Base, engine, get_db

# Models and Schemas (relative import)
from .models import User, Resume
from .schemas import UserCreate, UserLogin

# Resume analysis utils (relative import)
from .utils.extract_text import extract_text_from_upload
from .utils.classify_resume import detect_role, analyze_resume_evidence
from .utils.match_jd import compare_resume_and_jd

# ========================
# App & OpenAI Setup
# ========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY not set in environment or .env file")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="AI Resume Analyzer")

# Create tables
Base.metadata.create_all(bind=engine)

# ========================
# Middleware
# ========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://resume-analyzer-app-1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MAX_BCRYPT_BYTES = 72

# ========================
# Register endpoint
# ========================
@app.post("/register")
def register(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        password_truncated = user.password.encode("utf-8")[:MAX_BCRYPT_BYTES].decode(
            "utf-8", errors="ignore"
        )
        hashed_password = hash_password(password_truncated)

        new_user = User(
            name=user.name,
            email=user.email,
            password_hash=hashed_password,
            role=user.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"msg": "User created successfully"}

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ========================
# Login endpoint
# ========================
@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    password_truncated = data.password.encode("utf-8")[:MAX_BCRYPT_BYTES].decode(
        "utf-8", errors="ignore"
    )
    if not verify_password(password_truncated, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "role": user.role}


# ========================
# Analyze Resume endpoint
# ========================
@app.post("/analyze")
async def analyze_resume(file: UploadFile):
    resume_text = await extract_text_from_upload(file)
    needs_ocr = len(resume_text.strip()) < 200
    role = detect_role(resume_text)
    found = []
    missing = []

    try:
        prompt = f"Analyze this resume and provide evidence-based insights:\n\n{resume_text[:2000]}"

        # ✅ timeout + new OpenAI API syntax
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume analyzer."},
                {"role": "user", "content": prompt},
            ],
            timeout=30,  # prevents infinite loading
        )
        ai_analysis = response.choices[0].message.content

    except Exception as e:
        import traceback

        traceback.print_exc()
        ai_analysis = f"Analysis generation failed: {str(e)}"

    analysis = analyze_resume_evidence(found, missing, role, resume_text[:2000])
    return {
        "role_type": role,
        "analysis": analysis,
        "ai_analysis": ai_analysis,
        "ocr_needed": needs_ocr,
    }


# ========================
# Compare Resume with JD
# ========================
@app.post("/compare_resume_jd")
async def compare_resume_jd(resume: UploadFile, jd_text: str = Form(...)):
    resume_text = await extract_text_from_upload(resume)
    if not jd_text or len(jd_text.strip()) < 30:
        return {"error": "Job description text is too short or missing."}

    comparison = compare_resume_and_jd(resume_text, jd_text)
    return {"comparison_result": comparison}


# ========================
# Test endpoint
# ========================
@app.get("/test")
def test():
    return {"msg": "Server is running ✅"}
