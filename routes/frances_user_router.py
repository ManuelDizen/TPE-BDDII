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