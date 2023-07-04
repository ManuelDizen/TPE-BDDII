from fastapi import APIRouter, Depends, HTTPException, Request, Response
from config import get_frances_user_dao
from dao.frances_user_dao import FrancesUserDao
router = APIRouter(prefix="/FRA",)

@router.post(
    "/account",
    status_code=200, #TODO: Change for DTO, testing purposes
    responses={
        500:{"description":"internal server error"}
    },
)
async def create_user(
    name:str,
    frances_user_dao: FrancesUserDao = Depends(get_frances_user_dao)
):
    new = frances_user_dao.create_user(name)
    print(new)
    return Response(
        status_code=201,
        #TODO: location
    )

@router.get(
    "/{cbu}",
    status_code=200,
    responses={
        404: {"description":"not found"},
    },
)
async def get_user_by_cbu(
    cbu:str, 
    frances_user_dao: FrancesUserDao = Depends(get_frances_user_dao)
):
    user = frances_user_dao.get_user_by_cbu(cbu)
    if "cbu" not in user["docs"][0]:
        raise HTTPException(404, "not found")
    return user

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
    frances_user_dao: FrancesUserDao = Depends(get_frances_user_dao)
):
    check = frances_user_dao.deposit_to_account(cbu, amount)
    if check == 404:
        raise HTTPException(404, "Account does no texist")
    elif check == -1:
        raise HTTPException(400, "error en http request")
    return Response(
        status_code=200
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
    frances_user_dao: FrancesUserDao = Depends(get_frances_user_dao)
):
    check = frances_user_dao.extract_from_account(cbu, amount)
    if check == 400:
        raise HTTPException(400, "Not enough funds")
    if check == -1:
        raise HTTPException(400, "Error in extraction")
    return Response(
        status_code=200
    )