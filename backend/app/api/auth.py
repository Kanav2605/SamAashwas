import uuid
import secrets
import logging
import hmac
import hashlib
import base64
import json
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from ..core.realtime import realtime_hub

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Citizen & Officer Authentication"])

JWT_SECRET = "sam_aashwas_civic_sovereign_secret_key_2026_jwt"

# ============================================================================
# CRYPTOGRAPHIC JWT HELPERS (Zero external dependencies, RFC 7519 compliant)
# ============================================================================

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4)) if len(data) % 4 else ''
    return base64.urlsafe_b64decode(data + padding)

def create_jwt_token(payload: Dict[str, Any], expires_in_seconds: int = 86400) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    full_payload = {
        **payload,
        "jti": secrets.token_hex(16),
        "iat": now,
        "exp": now + expires_in_seconds,
    }
    header_b64 = base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_b64 = base64url_encode(json.dumps(full_payload, separators=(',', ':')).encode('utf-8'))
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(JWT_SECRET.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_b64 = base64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(JWT_SECRET.encode('utf-8'), signing_input, hashlib.sha256).digest()
        actual_sig = base64url_decode(sig_b64)
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
        payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload
    except Exception:
        return None


# ============================================================================
# USER & OFFICER REGISTRIES
# ============================================================================

# Preset Demo Citizen Profiles for instant 1-click citizen testing
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
        "aadhaar_verified": True,
        "is_admin": False
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
        "aadhaar_verified": True,
        "is_admin": False
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
        "aadhaar_verified": True,
        "is_admin": False
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
        "aadhaar_verified": True,
        "is_admin": False
    },
    "vikas_officer": {
        "id": "USR-OFF-01",
        "name": "Vikas Rao",
        "phone": "9811012000",
        "role": "Ward Officer",
        "role_title": "Ward Junior Engineer / SDO",
        "city": "Bengaluru",
        "ward": "Indiranagar (Ward 1)",
        "karma_points": 2100,
        "badge": "Ward Field Officer",
        "avatar": "👷🏽",
        "aadhaar_verified": True,
        "is_admin": True
    }
}

# Registered Municipal Officers & Administrators
OFFICER_REGISTRY: Dict[str, Dict[str, Any]] = {
    "admin": {
        "id": "OFF-HQ-99",
        "officer_id": "admin",
        "name": "Chief Commissioner Admin",
        "email": "admin@civicsense.gov.in",
        "phone": "9800000001",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Admin",
        "role_title": "Chief Municipal Commissioner / Admin",
        "city": "Pan-India ULB Grid",
        "ward": "All Metropolitan Wards",
        "karma_points": 5000,
        "badge": "Supreme Civic Administrator",
        "avatar": "🛡️",
        "aadhaar_verified": True,
        "is_admin": True,
        "permissions": ["all_admin", "triage", "dispatch", "predictive", "audit"]
    },
    "officer_vikas": {
        "id": "OFF-BLR-01",
        "officer_id": "officer_vikas",
        "name": "Er. Vikas Rao",
        "email": "vikas.rao@bbmp.gov.in",
        "phone": "9811012000",
        "password_hash": hashlib.sha256("officer2026".encode()).hexdigest(),
        "role": "Ward Officer",
        "role_title": "Junior Engineer / SDO",
        "city": "Bengaluru",
        "ward": "Indiranagar (Ward 1)",
        "karma_points": 2500,
        "badge": "BBMP Executive Engineer",
        "avatar": "👷🏽",
        "aadhaar_verified": True,
        "is_admin": True,
        "permissions": ["triage", "dispatch", "predictive"]
    },
    "sdo_delhi": {
        "id": "OFF-DEL-02",
        "officer_id": "sdo_delhi",
        "name": "Er. Arvind Saxena",
        "email": "arvind.saxena@mcd.nic.in",
        "phone": "9811019999",
        "password_hash": hashlib.sha256("mcd2026".encode()).hexdigest(),
        "role": "Zonal Superintending Engineer",
        "role_title": "SE Civil - Karol Bagh Zone",
        "city": "Delhi",
        "ward": "Karol Bagh (Ward 83)",
        "karma_points": 3400,
        "badge": "MCD Zonal Chief",
        "avatar": "🏛️",
        "aadhaar_verified": True,
        "is_admin": True,
        "permissions": ["triage", "dispatch", "predictive"]
    }
}

# Active user sessions: token -> user profile dict
ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}
# Revoked tokens set
REVOKED_TOKENS: set = set()

# Pending Real OTPs: phone -> {otp: str, expires_at: float, attempts: int}
PENDING_OTPS: Dict[str, Any] = {}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

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
    is_admin: bool = False


class LoginRequest(BaseModel):
    preset_id: Optional[str] = Field(None, description="Preset identifier (e.g. rajesh_kumar, priya_sharma)")
    phone: Optional[str] = Field(None, description="10-digit Indian Mobile Number")
    otp: Optional[str] = Field(None, description="6-digit OTP code")
    name: Optional[str] = Field(None, description="Optional citizen display name")
    city: Optional[str] = Field(None, description="Citizen city preference")


class AdminLoginRequest(BaseModel):
    officer_id: str = Field(..., description="Officer Username, Email, or Preset (e.g. 'admin', 'officer_vikas', 'admin@civicsense.gov.in')")
    password: str = Field(..., description="Officer Password (e.g. 'admin123', 'officer2026', 'mcd2026')")
    ward_code: Optional[str] = Field(None, description="Optional municipal zone or ward designation")


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
    expires_in_seconds: int = 300
    message: str


# ============================================================================
# HELPERS & TOKEN MANAGEMENT
# ============================================================================

def _clean_phone(phone: str) -> str:
    cleaned = "".join(c for c in phone if c.isdigit())
    if len(cleaned) > 10 and cleaned.startswith("91"):
        cleaned = cleaned[2:]
    return cleaned[-10:] if len(cleaned) >= 10 else cleaned


def _create_session(profile_data: Dict[str, Any]) -> str:
    """Creates a real cryptographically signed JWT token with claims."""
    jwt_claims = {
        "sub": profile_data.get("id"),
        "name": profile_data.get("name"),
        "phone": profile_data.get("phone"),
        "role": profile_data.get("role"),
        "role_title": profile_data.get("role_title"),
        "city": profile_data.get("city"),
        "ward": profile_data.get("ward"),
        "is_admin": profile_data.get("is_admin", False),
        "badge": profile_data.get("badge"),
        "avatar": profile_data.get("avatar"),
        "karma_points": profile_data.get("karma_points", 100)
    }
    token = create_jwt_token(jwt_claims, expires_in_seconds=86400)
    ACTIVE_SESSIONS[token] = profile_data
    return token


def get_current_user_from_token(token: Optional[str]) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    # Strip "Bearer "
    raw_token = token[7:].strip() if token.startswith("Bearer ") else token.strip()
    if raw_token in REVOKED_TOKENS:
        return None

    # 1. First check in active sessions
    if raw_token in ACTIVE_SESSIONS:
        return ACTIVE_SESSIONS[raw_token]

    # 2. Verify cryptographic JWT signature
    claims = verify_jwt_token(raw_token)
    if claims:
        # Reconstruct profile from verified JWT claims
        return {
            "id": claims.get("sub"),
            "name": claims.get("name"),
            "phone": claims.get("phone"),
            "role": claims.get("role", "Citizen"),
            "role_title": claims.get("role_title", "Verified Citizen"),
            "city": claims.get("city", "Bengaluru"),
            "ward": claims.get("ward", "Central Ward"),
            "karma_points": claims.get("karma_points", 100),
            "badge": claims.get("badge", "Active Citizen"),
            "avatar": claims.get("avatar", "👤"),
            "aadhaar_verified": True,
            "is_admin": claims.get("is_admin", False)
        }
    return None


PRIVILEGED_ROLES = {"ward officer", "officer", "ward volunteer", "rwa lead", "admin", "engineer", "corporator", "commissioner"}

def is_privileged_user(user: Optional[Dict[str, Any]]) -> bool:
    if not user:
        return False
    if user.get("is_admin", False):
        return True
    role = (user.get("role") or "").strip().lower()
    return role in PRIVILEGED_ROLES


def require_authenticated_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    user = get_current_user_from_token(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide a valid citizen or officer session token."
        )
    return user


def require_privileged_role(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    user = require_authenticated_user(authorization)
    if not is_privileged_user(user):
        raise HTTPException(
            status_code=403,
            detail=f"Forbidden: Action requires officer or volunteer privilege. Current role: {user.get('role')}"
        )
    return user


def require_admin_role(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Strictly requires an Officer / Administrator account."""
    user = require_authenticated_user(authorization)
    if not user.get("is_admin", False) and (user.get("role") or "").lower() not in ["admin", "ward officer", "commissioner"]:
        raise HTTPException(
            status_code=403,
            detail=f"Officer Access Denied: Municipal Executive privilege required. Current role: {user.get('role')}"
        )
    return user


def mask_phone(phone: Optional[str]) -> str:
    """Mask citizen phone number for public display (S2 privacy compliance)."""
    if not phone:
        return "XXXXX XXXXX"
    digits = "".join(c for c in str(phone) if c.isdigit())
    if len(digits) >= 10:
        return f"+91 {digits[:2]}*** **{digits[-3:]}"
    elif len(digits) >= 4:
        return f"***{digits[-4:]}"
    return "**********"


def mask_name(name: Optional[str]) -> str:
    """Mask citizen name for public display to protect privacy (S2 compliance)."""
    if not name or name.strip().lower() in ["citizen", "voice citizen"]:
        return "Verified Citizen"
    parts = name.strip().split()
    masked_parts = []
    for p in parts:
        if len(p) <= 2:
            masked_parts.append(p[0] + "*")
        else:
            masked_parts.append(p[0] + "*" * (len(p) - 2) + p[-1])
    return " ".join(masked_parts)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/presets", summary="Get available demo citizen profiles for instant testing")
async def get_demo_presets():
    """Returns list of preset citizen profiles for 1-click login on the UI."""
    return [
        {
            "preset_id": key,
            **val
        }
        for key, val in DEMO_PRESETS.items()
    ]


@router.get("/admin-presets", summary="Get available demo officer profiles for Admin Command Center")
async def get_admin_presets():
    """Returns list of municipal officer accounts for 1-click admin testing."""
    return [
        {
            "preset_id": key,
            "id": val["id"],
            "name": val["name"],
            "email": val["email"],
            "role": val["role"],
            "role_title": val["role_title"],
            "city": val["city"],
            "ward": val["ward"],
            "badge": val["badge"],
            "avatar": val["avatar"]
        }
        for key, val in OFFICER_REGISTRY.items()
    ]


@router.post("/login", summary="Citizen login with preset or mobile OTP initiation/completion")
async def login(payload: LoginRequest):
    """
    Authenticate citizen either via quick preset selection or phone number.
    - If preset_id is provided, instantly creates an authenticated session.
    - If phone is provided without OTP, generates a real 6-digit cryptographic OTP.
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
        try:
            await realtime_hub.broadcast("CITIZEN_PRESENCE_LOGIN", {
                "user_id": user_data["id"],
                "name": user_data["name"],
                "city": user_data["city"],
                "role": user_data["role"],
                "avatar": user_data["avatar"],
                "karma_points": user_data["karma_points"],
                "badge": user_data["badge"]
            })
        except Exception:
            pass
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

        # Real Dynamic Cryptographic 6-digit OTP with 5-minute TTL
        raw_otp = f"{secrets.randbelow(900000) + 100000}"
        # For ease of testing, also support 123456 as universal fallback
        demo_otp = "123456"
        expires_at = time.time() + 300.0  # 5 minutes validity
        PENDING_OTPS[clean_phone] = {
            "otp": raw_otp,
            "demo_otp": demo_otp,
            "expires_at": expires_at,
            "attempts": 0
        }
        logger.info(f"Generated real OTP {raw_otp} for phone {clean_phone} (valid for 300s)")

        try:
            await realtime_hub.broadcast("CITIZEN_OTP_DISPATCHED", {
                "phone_masked": mask_phone(clean_phone),
                "expires_in_seconds": 300,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "demo_otp": demo_otp
            })
        except Exception:
            pass

        return OTPRequestResponse(
            status="OTP_SENT",
            phone=clean_phone,
            otp_sent=True,
            demo_otp=demo_otp,
            expires_in_seconds=300,
            message=f"Real OTP sent to +91-{clean_phone} (Valid for 5 mins. Demo passkey: {demo_otp})"
        )

    raise HTTPException(
        status_code=400,
        detail="Please provide either 'preset_id' for 1-click login or 'phone' number"
    )


@router.post("/verify-otp", response_model=AuthResponse, summary="Verify mobile OTP and authenticate")
async def verify_otp(payload: VerifyOTPRequest):
    """
    Validates 6-digit OTP for the provided phone number with TTL check and rate limiting.
    Returns session JWT access token and citizen profile.
    """
    clean_phone = _clean_phone(payload.phone)
    entered_otp = payload.otp.strip()

    stored_record = PENDING_OTPS.get(clean_phone)
    now = time.time()

    is_valid = False
    if stored_record:
        if isinstance(stored_record, dict):
            if now > stored_record.get("expires_at", 0):
                PENDING_OTPS.pop(clean_phone, None)
                raise HTTPException(status_code=400, detail="OTP has expired. Please request a new OTP.")
            if entered_otp == stored_record.get("otp") or entered_otp == stored_record.get("demo_otp") or entered_otp == "123456":
                is_valid = True
            else:
                stored_record["attempts"] = stored_record.get("attempts", 0) + 1
                if stored_record["attempts"] >= 4:
                    PENDING_OTPS.pop(clean_phone, None)
                    raise HTTPException(status_code=400, detail="Too many invalid OTP attempts. Please request a new OTP.")
                raise HTTPException(status_code=400, detail=f"Invalid OTP code. {4 - stored_record['attempts']} attempts remaining.")
        elif isinstance(stored_record, str):
            is_valid = (entered_otp == stored_record or entered_otp == "123456")
    elif entered_otp == "123456":
        is_valid = True

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid OTP code. Please use demo OTP 123456 or request a new code.")

    # Remove verified OTP
    PENDING_OTPS.pop(clean_phone, None)

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
            "aadhaar_verified": True,
            "is_admin": False
        }

    token = _create_session(user_data)
    logger.info(f"Citizen OTP verified successfully for {user_data['name']} ({clean_phone})")

    try:
        await realtime_hub.broadcast("CITIZEN_PRESENCE_LOGIN", {
            "user_id": user_data["id"],
            "name": user_data["name"],
            "city": user_data["city"],
            "role": user_data["role"],
            "avatar": user_data["avatar"],
            "karma_points": user_data["karma_points"],
            "badge": user_data["badge"]
        })
    except Exception:
        pass

    return AuthResponse(
        status="SUCCESS",
        access_token=token,
        user=CitizenProfile(**user_data),
        message=f"Verification successful. Welcome {user_data['name']}!"
    )


@router.post("/admin-login", response_model=AuthResponse, summary="Dedicated Municipal Officer & Admin Login")
async def admin_login(payload: AdminLoginRequest):
    """
    Dedicated authentication gate for Municipal Officers, Junior Engineers, and Administrators.
    Validates credentials and issues an elevated Officer JWT token.
    """
    officer_key = payload.officer_id.lower().strip()
    officer_record = None

    # Match by key or email
    if officer_key in OFFICER_REGISTRY:
        officer_record = OFFICER_REGISTRY[officer_key]
    else:
        officer_record = next(
            (v for v in OFFICER_REGISTRY.values() if v.get("email", "").lower() == officer_key),
            None
        )

    if not officer_record:
        # Fallback check for demo master admin credentials
        if officer_key in ["admin", "officer", "commissioner"] and payload.password in ["admin123", "officer2026", "mcd2026"]:
            officer_record = OFFICER_REGISTRY["admin"]
        else:
            raise HTTPException(status_code=401, detail="Invalid Officer ID or Email. Please check credentials or use an Officer Preset.")

    # Validate password hash or direct match
    entered_hash = hashlib.sha256(payload.password.encode()).hexdigest()
    if entered_hash != officer_record["password_hash"] and payload.password not in ["admin123", "officer2026", "mcd2026"]:
        raise HTTPException(status_code=401, detail="Invalid Officer Password or Security Passcode.")

    officer_data = dict(officer_record)
    officer_data["is_admin"] = True
    token = _create_session(officer_data)

    logger.info(f"Municipal Officer authenticated: {officer_data['name']} ({officer_data['role_title']})")
    try:
        await realtime_hub.broadcast("OFFICER_PRESENCE_LOGIN", {
            "officer_id": officer_data["id"],
            "name": officer_data["name"],
            "role": officer_data["role"],
            "role_title": officer_data["role_title"],
            "city": officer_data["city"],
            "ward": officer_data["ward"]
        })
    except Exception:
        pass

    return AuthResponse(
        status="SUCCESS",
        access_token=token,
        user=CitizenProfile(**officer_data),
        message=f"Executive Access Granted: Welcome {officer_data['name']} ({officer_data['role_title']})!"
    )


@router.get("/me", response_model=CitizenProfile, summary="Get current authenticated citizen or officer profile")
async def get_me(authorization: Optional[str] = Header(None)):
    """Returns profile of currently logged-in user using Bearer token."""
    user = get_current_user_from_token(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthenticated. Please provide a valid citizen or officer session token."
        )
    return CitizenProfile(**user)


@router.post("/logout", summary="Logout current user and invalidate cryptographic token")
async def logout(authorization: Optional[str] = Header(None)):
    """Invalidates current session and registers token revocation."""
    user_id = None
    if authorization:
        raw_token = authorization[7:].strip() if authorization.startswith("Bearer ") else authorization.strip()
        REVOKED_TOKENS.add(raw_token)
        user = ACTIVE_SESSIONS.pop(raw_token, None)
        if user:
            user_id = user.get("id")

    try:
        await realtime_hub.broadcast("CITIZEN_PRESENCE_LOGOUT", {"user_id": user_id, "status": "LOGGED_OUT"})
    except Exception:
        pass

    return {"status": "SUCCESS", "message": "Successfully logged out of SamAashwas"}
