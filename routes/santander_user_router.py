from fastapi import APIRouter, Depends, HTTPException, Request, Response
from models.santander_user import SantanderUserDTO
from config import get_santander_transfer_dao, get_santander_user_dao
from dao.santander_user_dao import SantanderUserDao
from dao.santander_transfer_dao import SantanderTransferDao

router = APIRouter(prefix="/STD",
                   tags=["Banco Santander"])

@router.get(
    "/cbu/{cbu}",
    response_model = SantanderUserDTO,
    responses={
        404: {"description": "User not found"},
        403: {"description": "Forbidden operation"},
    },
)
async def get_user_by_cbu(
    cbu:str,
    request:Request,
    santander_user_dao: SantanderUserDao = Depends(get_santander_user_dao),
):
    user = santander_user_dao.get_user_by_cbu(cbu)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return SantanderUserDTO.from_user(user=user, request=request)

@router.get(
    "/name/{name}",
    response_model = SantanderUserDTO,
    responses={
        404: {"description": "User not found"},
        403: {"description": "Forbidden operation"},
    },
)
async def get_user_by_cbu(
    name:str,
    request:Request,
    santander_user_dao: SantanderUserDao = Depends(get_santander_user_dao),
):
    user = santander_user_dao.get_user_by_name(name)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return SantanderUserDTO.from_user(user=user, request=request)

@router.post(
    "/account", 
    status_code=201,
    responses={409: {"description": "User already exists"}},
)
async def create_user(
    name:str,
    request: Request,
    santander_user_dao: SantanderUserDao = Depends(get_santander_user_dao),
):
    new = santander_user_dao.create_user(name)
    if new is None:
        raise HTTPException(status_code=409, detail="User already exists")
    location = request.url_for("santander_user_dao.get_user_by_cbu", cbu=new.cbu)
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
    santander_user_dao: SantanderUserDao = Depends(get_santander_user_dao),
):
    user = santander_user_dao.get_user_by_cbu(cbu)
    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    if int(user.balance) < amount:
        raise HTTPException(status_code=409, detail="Not enough funds")
    
    santander_user_dao.extract_from_account(cbu, amount)
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
    santander_user_dao: SantanderUserDao = Depends(get_santander_user_dao),
):
    user = santander_user_dao.get_user_by_cbu(cbu)
    if user is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    santander_user_dao.deposit_to_account(cbu, amount)
    location = request.url_for("get_user_by_cbu", cbu=cbu)
    location = str(location)
    return Response(
        status_code=200,
        headers={
            "Location": location
        },
    )

""" @router.post(
    '/transfer',
    status_code=200,
    responses={
        404:{"description":"dst_cbu not found in given bank"},
        404:{"description":"no dst_bank with that code"},
    }
)
async def send_transfer_internal_std(
    src_cbu:str,
    src_bank:str,
    dst_cbu:str,
    dst_bank:str,
    amount:int,
    request:Request,
    santander_user_dao: SantanderUserDao = Depends(get_santander_user_dao),
    santander_transfer_dao: SantanderTransferDao = Depends(get_santander_transfer_dao)
):
    # TODO: Voy a armar este método para hacer transferencias internas entre cuentas del galicia
    # Cuando tenga armada la parte de PIX, ahi me puedo poner a 
    sending_user = santander_user_dao.get_user_by_cbu(src_cbu)
    if sending_user is None:
        raise HTTPException(status_code=404, detail="src_cbu not found")
    if sending_user.balance < amount:
        raise HTTPException(status_code=404, detail="insufficient funds from sender")
    #TODO: Cambiar el código

    receiving_user = santander_user_dao.get_user_by_cbu(dst_cbu)
    if receiving_user is None:
        raise HTTPException(status_code=404, detail="dst_cbu not found")

    transfer = santander_transfer_dao.create_transfer(src_cbu, dst_cbu, src_bank, dst_bank, amount)
    if transfer is None:
        raise HTTPException(status_code=400, detail="Internal server error")
    santander_user_dao.transfer_to_account(transfer.id, src_cbu)
    santander_user_dao.receive_transfer(transfer.id, dst_cbu) 
    #TODO: estas dos líneas de arriba son las que están mal digamos. 
    #Cuando se maneje desde PIX, no se tendría que usar esta función ni siquiera
    santander_user_dao.extract_from_account(src_cbu, amount)
    santander_user_dao.deposit_to_account(dst_cbu, amount)


    return Response(
        status_code=200,
    ) """

@router.get(
    "/balance/{cbu}",
    status_code=200,
    responses={
        404: {"description":"not found"},
    },
)
async def get_balance_by_cbu(
    cbu:str, 
    santander_user_dao: SantanderUserDao = Depends(get_santander_user_dao)
):
    user = santander_user_dao.get_user_by_cbu(cbu)
    if user is None:
        raise HTTPException(404, "not found")
    return {"balance":user.balance, "cbu":cbu}