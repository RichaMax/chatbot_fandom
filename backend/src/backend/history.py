from fastapi import APIRouter

router = APIRouter()

@router.get("/history")
async def get_history():
    # Would need a cookie to recognize the user
    return 