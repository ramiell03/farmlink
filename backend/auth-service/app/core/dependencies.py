from fastapi import Depends, HTTPException, status, Header
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, JWT_ALGORITHM
from typing import Optional


def get_current_user(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Authorization header missing" 
        )
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
                )
            
        return {"email":email, "role":role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
def require_roles(allowed_roles:list):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: insufficient permissions"
            )
        return user
    return role_checker
    