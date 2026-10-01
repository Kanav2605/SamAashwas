import uuid
import secrets
import logging
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Citizen Authentication & Identity"])

# In-memory session store & registered users
# Preset Demo Profiles for instant 1-click civic testing
DEMO_PRESETS: Dict[str, Dict[str, Any]] = {
    "rajesh_kumar": {
        "id": "USR-BLR-01",
        "name": "Rajesh Kumar",
        "phone": "9876543210",
        "role": "Citizen",
        "role_title": "Active Citizen",
        "city": "Bengaluru",
        "ward": "Indiranagar (Ward 1)",
        "karma_points": 850,
        "badge": "Gold Civic Sentinel",
        "avatar": "👨🏽",
        "aadhaar_verified": True
    },
    "priya_sharma": {
        "id": "USR-DEL-02",
        "name": "Priya Sharma",
        "phone": "9811012002",
        "role": "Ward Volunteer",
        "role_title": "Ward Civic Volunteer",
        "city": "Delhi",
        "ward": "Karol Bagh (Ward 83)",
        "karma_points": 1240,
        "badge": "Star Civic Champion",
        "avatar": "👩🏽",
        "aadhaar_verified": True
    },
    "aarav_sharma": {
        "id": "USR-MUM-03",
        "name": "Aarav Sharma",
        "phone": "9811099888",
        "role": "Citizen",
        "role_title": "Registered Resident",
        "city": "Mumbai",
        "ward": "Bandra West (Ward H/W)",
        "karma_points": 920,
        "badge": "Silver Shield",
        "avatar": "🧑🏽",
        "aadhaar_verified": True
    },
    "sunita_patel": {
        "id": "USR-PUN-04",
        "name": "Sunita Patel",
        "phone": "9822054321",
        "role": "RWA Lead",
        "role_title": "Resident Welfare Assoc. Lead",
        "city": "Pune",
        "ward": "Shivajinagar (Ward 12)",
        "karma_points": 1650,
        "badge": "Community Pillar",
        "avatar": "👩🏽‍💼",
        "aadhaar_verified": True
    }
}

# Active user sessions: token -> user profile dict
ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}
# Pending OTPs: phone -> otp string
PENDING_OTPS: Dict[str, str] = {}


class CitizenProfile(BaseModel):
    id: str
    name: str
    phone: str
    role: str
    role_title: str
    city: str
    ward: str
    karma_points: int
    badge: str
    avatar: str
    aadhaar_verified: bool = True


class LoginRequest(BaseModel):
    preset_id: Optional[str] = Field(None, description="Preset identifier (e.g. rajesh_kumar, priya_sharma)")
    phone: Optional[str] = Field(None, description="10-digit Indian Mobile Number")
    otp: Optional[str] = Field(None, description="6-digit OTP code")
    name: Optional[str] = Field(None, description="Optional citizen display name")
    city: Optional[str] = Field(None, description="Citizen city preference")


class VerifyOTPRequest(BaseModel):
    phone: str = Field(..., description="10-digit mobile number")
    otp: str = Field(..., description="6-digit verification OTP")
    name: Optional[str] = Field(None, description="Citizen name if new user")
    city: Optional[str] = Field(None, description="Citizen city")


class AuthResponse(BaseModel):
    status: str
    access_token: str
    token_type: str = "bearer"
    user: CitizenProfile
    message: str


class OTPRequestResponse(BaseModel):
    status: str
    phone: str
    otp_sent: bool
    demo_otp: str
    message: str


def _clean_phone(phone: str) -> str:
    cleaned = "".join(c for c in phone if c.isdigit())
    if len(cleaned) > 10 and cleaned.startswith("91"):
        cleaned = cleaned[2:]
    return cleaned[-10:] if len(cleaned) >= 10 else cleaned


def _create_session(profile_data: Dict[str, Any]) -> str:
    token = f"sam_tok_{secrets.token_hex(16)}"
    ACTIVE_SESSIONS[token] = profile_data
    return token


def get_current_user_from_token(token: Optional[str]) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    # Support "Bearer <token>"
    if token.startswith("Bearer "):
        token = token[7:].strip()
    return ACTIVE_SESSIONS.get(token)


@router.get("/presets", summary="Get available demo citizen profiles for instant testing")
async def get_demo_presets():
    """
    Returns list of preset citizen profiles for 1-click login on the UI.
    """
    return [
        {
            "preset_id": key,
            **val
        }
        for key, val in DEMO_PRESETS.items()
    ]


@router.post("/login", summary="Citizen login with preset or mobile OTP initiation/completion")
async def login(payload: LoginRequest):
    """
    Authenticate citizen either via quick preset selection or phone number.
    - If preset_id is provided, instantly creates an authenticated session.
    - If phone is provided without OTP, generates/returns demo OTP.
    - If phone and OTP are provided, verifies and returns session.
    """
    # 1. Preset 1-Click Login
    if payload.preset_id:
        preset_key = payload.preset_id.lower().strip()
        if preset_key not in DEMO_PRESETS:
            raise HTTPException(
                status_code=400,
                detail=f"Preset '{payload.preset_id}' not found. Available: {list(DEMO_PRESETS.keys())}"
            )
        user_data = dict(DEMO_PRESETS[preset_key])
        token = _create_session(user_data)
        logger.info(f"Citizen authenticated via preset: {user_data['name']} ({user_data['phone']})")
        return AuthResponse(
            status="SUCCESS",
            access_token=token,
            user=CitizenProfile(**user_data),
            message=f"Namaste {user_data['name']}! Logged in successfully."
        )

    # 2. Phone Login
    if payload.phone:
        clean_phone = _clean_phone(payload.phone)
        if len(clean_phone) < 10:
            raise HTTPException(status_code=400, detail="Please enter a valid 10-digit mobile number")

        # If OTP provided in login payload -> complete verification
        if payload.otp:
            return await verify_otp(VerifyOTPRequest(
                phone=clean_phone,
                otp=payload.otp,
                name=payload.name,
                city=payload.city
            ))

        # Otherwise generate OTP
        demo_otp = "123456"
        PENDING_OTPS[clean_phone] = demo_otp
        logger.info(f"Generated OTP {demo_otp} for phone {clean_phone}")
        return OTPRequestResponse(
            status="OTP_SENT",
            phone=clean_phone,
            otp_sent=True,
            demo_otp=demo_otp,
            message=f"OTP sent to +91-{clean_phone}. (Demo code: 123456)"
        )

    raise HTTPException(
        status_code=400,
        detail="Please provide either 'preset_id' for 1-click login or 'phone' number"
    )


@router.post("/verify-otp", response_model=AuthResponse, summary="Verify mobile OTP and authenticate")
async def verify_otp(payload: VerifyOTPRequest):
    """
    Validates 6-digit OTP for the provided phone number.
    Returns session access token and citizen profile.
    """
    clean_phone = _clean_phone(payload.phone)
    entered_otp = payload.otp.strip()

    valid_otp = PENDING_OTPS.get(clean_phone, "123456")
    # Accept either stored OTP or universal test OTP "123456"
    if entered_otp != valid_otp and entered_otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP code. Please use demo OTP 123456.")

    # Check if this phone matches any known preset
    matching_preset = next((v for v in DEMO_PRESETS.values() if v["phone"] == clean_phone), None)
    if matching_preset:
        user_data = dict(matching_preset)
    else:
        user_data = {
            "id": f"USR-{uuid.uuid4().hex[:6].upper()}",
            "name": payload.name or f"Citizen (+91 {clean_phone[-4:]})",
            "phone": clean_phone,
            "role": "Citizen",
            "role_title": "Verified Citizen",
            "city": payload.city or "Bengaluru",
            "ward": "Central Ward",
            "karma_points": 100,
            "badge": "Active Citizen",
            "avatar": "👤",
            "aadhaar_verified": True
        }

    token = _create_session(user_data)
    if clean_phone in PENDING_OTPS:
        del PENDING_OTPS[clean_phone]

    logger.info(f"Citizen OTP verified for {user_data['name']} ({clean_phone})")
    return AuthResponse(
        status="SUCCESS",
        access_token=token,
        user=CitizenProfile(**user_data),
        message=f"Verification successful. Welcome {user_data['name']}!"
    )


@router.get("/me", response_model=CitizenProfile, summary="Get current authenticated citizen profile")
async def get_me(authorization: Optional[str] = Header(None)):
    """
    Returns profile of currently logged-in citizen using Bearer token.
    """
    user = get_current_user_from_token(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthenticated. Please provide a valid citizen session token."
        )
    return CitizenProfile(**user)


@router.post("/logout", summary="Logout current citizen")
async def logout(authorization: Optional[str] = Header(None)):
    """
    Invalidates current citizen session.
    """
    if authorization:
        token = authorization[7:].strip() if authorization.startswith("Bearer ") else authorization.strip()
        ACTIVE_SESSIONS.pop(token, None)
    return {"status": "SUCCESS", "message": "Successfully logged out of SamAashwas"}
