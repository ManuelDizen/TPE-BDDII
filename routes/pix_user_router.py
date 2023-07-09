from fastapi import APIRouter, Depends, HTTPException, Request, Response
from config import get_galicia_transfer_dao, get_galicia_user_dao, get_pix_user_dao, get_santander_user_dao, get_santander_transfer_dao, get_frances_user_dao, get_frances_transfer_dao
from dao.pix_user_dao import PixUserDao
from models.pix_user import PixUserDTO

router = APIRouter(prefix="/PIX",
                   tags=["Pix"]
                )

@router.get(
    '/user',
    status_code=200,
    responses={
        404: {"description":"user not found"},
    }
)
async def get_user_by_cuit(
    cuit:str,
    pix_user_dao:PixUserDao = Depends(get_pix_user_dao)
):
    user = pix_user_dao.get_from_cuit(cuit)
    if user == -1:
        raise HTTPException(404, "User not found")
    else:  
        return PixUserDTO(user[1], user[2], user[3], user[4])

@router.post(
    '/user',
    status_code=201,
    responses={
        422: {"description":"User already exists"},   
    }
)
async def create_user(
    request: Request,
    cuit: str, 
    name: str, 
    email: str = None,
    phone: str = None,
    pix_user_dao: PixUserDao = Depends(get_pix_user_dao)
):
    check = pix_user_dao.create_pix_user(cuit, name, email, phone)
    if check == -1:
        raise HTTPException(422, "User already exists")
    else:
        return Response(
            status_code=201, #TODO: Location
    )

@router.post(
    '/{cbu}/bank_account',
    status_code = 201,
    responses={
        404:{"description":"user not found in pix"},
        404:{"description":"Bank code is invalid"}
    }
)
async def add_bank_account_to_user(
    user_cuit:str,
    cbu:str, 
    bank_code:str,
    pix_user_dao: PixUserDao = Depends(get_pix_user_dao)
):
    result = pix_user_dao.create_pix_bank_account(user_cuit, 
                                                  get_id_from_name(bank_code), 
                                                  cbu)
    if result == -1:
        raise HTTPException(400, "User side error")
    return Response(
        status_code=201 #TODO: Location
    )



@router.post(
    '/transfer',
    status_code=200,
    responses={
        404:{"description":"dst_cbu not found in given bank"},
        404:{"description":"no dst_bank with that code"},
    }
)
async def send_transfer(
    src_cbu:str,
    src_bank:str,
    dst_cbu:str,
    dst_bank:str,
    amount:int,
    request:Request,
    pix_user_dao: PixUserDao = Depends(get_pix_user_dao)
):
    bank_id = get_id_from_name(src_bank)
    if bank_id == -1:
        raise HTTPException(404, "Bank not found")
    dao = get_user_dao_for_bank_id(bank_id)
    sender = dao.get_user_by_cbu(src_cbu)
    if sender is None or sender.balance < amount:
        raise HTTPException(404, "Bank not found")
    
    rcv_bank_id = get_id_from_name(dst_bank)
    if rcv_bank_id == -1:
        raise HTTPException(404, "Bank not found")
    rcv_dao = get_user_dao_for_bank_id(rcv_bank_id)
    receiver = rcv_dao.get_user_by_cbu(dst_cbu)
    if receiver is None:
        raise HTTPException(404, "Bank not found") #TODO: Corregir estas excepciones
    
    t_dao = get_transfer_dao_for_bank_id(bank_id)
    transfer = t_dao.create_transfer(src_cbu, dst_cbu, 
                                        get_name_from_id(bank_id),
                                        get_name_from_id(rcv_bank_id),
                                        amount)
    print(transfer)
    dao.transfer_to_account(transfer.id, src_cbu)
    dao.extract_from_account(src_cbu, amount)

    t_dao = get_transfer_dao_for_bank_id(rcv_bank_id)
    transfer = t_dao.create_transfer(src_cbu, dst_cbu, 
                                        get_name_from_id(bank_id),
                                        get_name_from_id(rcv_bank_id),
                                        amount)
    # Nota: Lo creo dos veces porque no puedo utilizar el mismo ID para ambas cosas
    rcv_dao.receive_transfer(transfer.id, dst_cbu) #Persiste en cuenta banco el id de la transaccion
    rcv_dao.deposit_to_account(dst_cbu, amount) # Aumenta balance de cuenta

    pix_user_dao.extract_from_account(src_bank, src_cbu, amount)
    pix_user_dao.add_to_account(dst_bank, dst_cbu, amount)

    return Response(
        status_code=201, #TODO: Location
    )


def get_transfer_dao_for_bank_id(bank_id:int):
    if bank_id == 0: 
        return get_galicia_transfer_dao()
    elif bank_id == 1:
        # STD (TODO: Change for new daos when created)
        return get_santander_transfer_dao()
        # return get_santander_user_dao()
    elif bank_id == 2:
        return get_frances_transfer_dao()
        # return get_frances_user_dao()

def get_user_dao_for_bank_id(bank_id:int):
    if bank_id == 0: 
        return get_galicia_user_dao()
    elif bank_id == 1:
        # STD (TODO: Change for new daos when created)
        return get_santander_user_dao()
        # return get_santander_user_dao()
    elif bank_id == 2:
        return get_frances_user_dao()
        # return get_frances_user_dao()

def get_name_from_id(id:int):
    if id == 0:
        return "GAL"
    elif id == 1:
        return "STD"
    elif id == 2:
        return "FRA"
    else:
        return -1
    
def get_id_from_name(name:str):
    if name == "GAL":
        return 0
    elif name == "STD":
        return 1
    elif name == "FRA":
        return 2
    else:
        return -1