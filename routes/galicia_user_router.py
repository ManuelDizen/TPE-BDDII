from fastapi import APIRouter, Depends, HTTPException, Request, Response
from models.galicia_user import GaliciaUserDTO
from config import get_galicia_user_dao
from dao.galicia_user_dao import GaliciaUserDao
router = APIRouter(prefix="/GAL",)

@router.get(
    "/{cbu}",
    response_model = GaliciaUserDTO,
    responses={
        404: {"description": "User not found"},
        403: {"description": "Forbidden operation"},
    },
)
async def get_user_by_cbu(
    cbu:str,
    request:Request,
    galicia_user_dao: GaliciaUserDao = Depends(get_galicia_user_dao),
):
    user = galicia_user_dao.get_user_by_cbu(cbu)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return GaliciaUserDTO.from_user(user=user, request=request)

@router.post(
    "/", 
    status_code=201,
    responses={409: {"description": "User already exists"}},
)
async def create_galicia_user(
    name:str,
    request: Request,
    galicia_user_dao: GaliciaUserDao = Depends(get_galicia_user_dao),
):
    new = galicia_user_dao.create_galicia_user(name)
    if new is None:
        raise HTTPException(status_code=409, detail="User already exists")
    return Response(
        status_code=201,
        headers={
            "Location": request.url_for(
                "get_user_by_cbu", cbu=new.cbu
            ) #TODO: Acá me está dejando crear sin problema pero me tira un error porque dice
                # "AttributeError: URL has no attribute "encoding"
        },
    )
