import secrets, hashlib
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import PasswordResetToken, User
from password_utils import hash_password, verify_password  


def hash_token(token: str) -> str:
    
    return hashlib.sha256(token.encode()).hexdigest()

def create_reset_token(db: Session, user_id: int, expires_minutes: int = 60):
    
    # Generate a reset token, store its hash, and return the raw token for email.
    
    raw_token = secrets.token_urlsafe(48)
    token_hash = hash_token(raw_token)
    expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
    pr = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        used=False
    )
    db.add(pr)
    db.commit()
    db.refresh(pr)
    return raw_token

def verify_and_consume_token(db: Session, user_id: int, token: str) -> bool:
    """
    Verify a reset token, ensure it's valid, unused, and not expired.
    Marks it as used if valid.
    """
    token_hash = hash_token(token)
    pr = db.query(PasswordResetToken).filter_by(
        user_id=user_id,
        token_hash=token_hash
    ).first()

    if not pr or pr.used or pr.expires_at < datetime.utcnow():
        return False

    pr.used = True
    db.add(pr)
    db.commit()
    return True
