from fastapi import APIRouter, Depends, HTTPException, Request, Response

router = APIRouter(prefix="/PIX",)

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
):
    
    return 0