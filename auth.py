from fastapi import Header, HTTPException, status

API_KEYS = {
    "admin-key": "admin",
    "user-key": "user"
}



def get_current_role(x_api_key: str = Header(None)):
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API-Key fehlt. Bitte X-API-Key im Header mitsenden."
        )

    role = API_KEYS.get(x_api_key)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültiger API-Key."
        )

    return role




def require_admin(role: str):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung. Nur Admins dürfen diese Operation ausführen."
        )

