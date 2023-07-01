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
    location = request.url_for("get_user_by_cbu", cbu=new.cbu)
    location = str(location)
    return Response(
        status_code=201,
        headers={
            "Location": location
        },
    )

@router.patch(
    '/{cbu}/extract',
    status_code=200,
    responses={
        404:{"description":"user doesn't exist"},
        409:{"description":"Not enough funds"}}
)
async def extract_from_account(
    cbu:str,
    amount:int,
    request: Request,
    galicia_user_dao: GaliciaUserDao = Depends(get_galicia_user_dao),
):
    user = galicia_user_dao.get_user_by_cbu(cbu)
    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    if user.balance < amount:
        raise HTTPException(status_code=409, detail="Not enough funds")
    
    galicia_user_dao.extract_from_account(user, amount)
    location = request.url_for("get_user_by_cbu", cbu=cbu)
    location = str(location)
    return Response(
        status_code=200,
        headers={
            "Location": location
        },
    )


@router.patch(
    '/{cbu}/deposit',
    status_code=200,
    responses={
        404:{"description":"user doesn't exist"},}
)
async def deposit_to_account(
    cbu:str,
    amount:int,
    request: Request,
    galicia_user_dao: GaliciaUserDao = Depends(get_galicia_user_dao),
):
    user = galicia_user_dao.get_user_by_cbu(cbu)
    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    galicia_user_dao.deposit_to_account(user, amount)
    location = request.url_for("get_user_by_cbu", cbu=cbu)
    location = str(location)
    return Response(
        status_code=200,
        headers={
            "Location": location #TODO: Acá me está dejando crear sin problema pero me tira un error porque dice
                # "AttributeError: URL has no attribute "encoding"
        },
    )