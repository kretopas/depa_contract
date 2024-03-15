# app/api.py

# ? owned module
from app.model import UserLoginSchema, UserRegister, UserEdit, OtpBaseSchema, OtpRequestSchema
from app.auth.auth_handler import create_access_token, create_refresh_token
from app.auth.auth_bearer import JWTBearer
from app.odoo.user import check_authenticate, reset_user_password, change_user_password, email_otp, check_duplicate_user
from app.odoo.signature import get_encoded_signature, sign_contractor_document, sign_document
from app.odoo.contractor import get_contractor_detail, register_contractor, update_contractor, revoke_contract, renew_contract
from app.odoo.document import get_contractor_waiting_documents, get_contractor_document_detail, get_contractor_signed_documents, get_preview_document
from app.odoo.employee import register_employee_certificate
from app.database import Otp
from app.helpers.logger import log

# ? import from outside
import os
import json
import pyotp
from pytz import timezone
from typing import Union
from fastapi import APIRouter ,FastAPI, Body, Depends, Form, File, UploadFile, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pymongo.collection import ReturnDocument

app = FastAPI(docs_url=None, redoc_url=None)
router = APIRouter(prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# ? user_group 9 => ประเภท Portal User
# ? user_group 1 => ประเภท Internal User

def get_now() -> datetime:
    #return (datetime.now(timezone('Asia/Bangkok')))
    return datetime.now()

@router.get("/", tags=["root"])
async def root() -> dict:
    return {"Detail": "API FOR DEPA CONTRACT APPLICATION."}

def decode_token_data(token: str) -> dict:
    jwt_bearer = JWTBearer()
    token_decoded = jwt_bearer.get_token_data(jwtoken=token)
    return token_decoded

@router.post("/login", tags=["authen"])
async def user_login(user: UserLoginSchema = Body(...)) -> Union[dict, bool]:
    user_id, user_group = check_authenticate(user.username, user.password)
    if user_id and user_group:
        if not check_otp_user_exists(user.username):
            otp_user = OtpBaseSchema(username=user.username)
            insert_otp_user(otp_user)
            log.info(f"Create OTP User [{user.username}]")
        return True
    return False

@router.post("/refresh", tags=["authen"])
async def refresh_token(token_data: dict = Body(...)) -> dict:
    refresh_token = token_data['token']
    token_decoded = decode_token_data(refresh_token)
    if token_decoded is not None:
        access_token = create_access_token(token_decoded['user_id'], token_decoded['user_group'], token_decoded['username'])
        return {"access_token": access_token}
    else:
        return False

@router.get("/user/detail", tags=["user"])
async def get_user_detail(token_data: dict = Depends(JWTBearer())) -> dict:
    user_group = token_data['user_group']
    if user_group == 9:
        return get_contractor_detail(token_data['user_id'])
    
@router.post("/user/update/withoutfile", tags=["user"])
async def update_user_detail_without_file(token_data: dict = Depends(JWTBearer()), user_data: str = Form(...)) -> bool:
    try:
        user_group = token_data['user_group']
        if user_group == 9:
            user_edit = UserEdit(json.loads(user_data))
            if update_contractor(token_data['user_id'], user_edit):
                log.info(f"User [{token_data['username']}] update (without file) complete!")
                return True
            else:
                log.info(f"User [{token_data['username']}] update (without file) failure!")
                return False
    except Exception as e:
        log.exception("User update (without file)")
        return False
    
@router.post("/user/update/withfile", tags=["user"])
async def update_user_detail_with_file(token_data: dict = Depends(JWTBearer()), user_data: str = Form(...), sign_img: UploadFile = File(...)) -> bool:
    try:
        user_group = token_data['user_group']
        if user_group == 9:
            user_edit = UserEdit(json.loads(user_data))
            encoded_signature = get_encoded_signature(sign_img)
            if update_contractor(token_data['user_id'], user_edit, encoded_signature):
                log.info(f"User [{token_data['username']}] update (with file) complete!")
                return True
            else:
                log.info(f"User [{token_data['username']}] update (with file) failure!")
                return False
    except Exception as e:
        log.exception("User update (with file)")
        return False

@router.post("/user/register", tags=["user"])
async def user_register(user_data: str = Form(...), sign_img: UploadFile = File(...)) -> Union[dict, bool]:
    try:
        user_register = UserRegister(json.loads(user_data))
        encoded_signature = get_encoded_signature(sign_img)
        if register_contractor(user_register, encoded_signature):
            log.info(f"User [{user_register.username}] register complete!")
            return True
        else:
            log.info(f"User [{user_register.username}] register failure!")
            return False
    except Exception as e:
        log.exception("User Register")
        return False
    
@router.post("/employee/certificate", tags=["employee"])
async def employee_certificate(request: Request) -> Union[dict, bool]:
    try:
        json_ = await request.json()
        user_id = json_['user_id']
        register = register_employee_certificate(user_id)
        if register:
            log.info(f"Employee User Id = [{user_id}] create certificate complete!")
        else:
            log.info(f"Employee User Id = [{user_id}] create certificate failure!")
        return register
    except Exception as e:
        log.exception("Employee Certificate")
        return False

@router.get("/doc/waiting", tags=['document'])
async def get_waiting_documents(token_data: dict = Depends(JWTBearer())) -> Union[list, bool]:
    user_group = token_data['user_group']
    if user_group == 9:
        documents = get_contractor_waiting_documents(user_id=token_data['user_id'])
        return documents
    
@router.get("/doc/complete", tags=['documents'])
async def get_signed_documents(token_data: dict = Depends(JWTBearer())) -> Union[list, bool]:
    user_group = token_data['user_group']
    if user_group == 9:
        documents = get_contractor_signed_documents(user_id=token_data['user_id'])
        return documents
    
@router.get("/doc/detail/{document_id}", tags=['document'])
async def get_document_detail(document_id: int, token_data: dict = Depends(JWTBearer())) -> Union[dict, bool]:
    user_group = token_data['user_group']
    if user_group == 9:
        document = get_contractor_document_detail(user_id=token_data['user_id'], document_id=document_id, waiting=True)
        return document
    
@router.get("/doc/complete/detail/{document_id}", tags=['document'])
async def get_signed_document_detail(document_id: int, token_data: dict = Depends(JWTBearer())) -> Union[dict, bool]:
    user_group = token_data['user_group']
    if user_group == 9:
        document = get_contractor_document_detail(user_id=token_data['user_id'], document_id=document_id, waiting=False)
        return document
    
@router.get("/doc/preview/{document_id}",dependencies=[Depends(JWTBearer())],tags=['document'])
async def preview_document(document_id: int) -> Union[str, bool]:
    preview_pdf = get_preview_document(document_id)
    return preview_pdf

@router.get("/doc/sign/{document_id}", tags=['document'])
async def approve_contract(document_id: int, token_data: dict = Depends(JWTBearer())) -> bool:
    user_group = token_data['user_group']
    if user_group == 9:
        sign_status = sign_contractor_document(token_data['user_id'], document_id)
        log.info(f"User [{token_data['username']}] signed document's id : {document_id}.")
        return sign_status
    
@router.get("/forget/{user}", tags=['user'])
def forget_password(user: str) -> Union[str, bool]:
    return reset_user_password(user)

@router.post("/user/password", tags=['user'])
async def change_password(request: Request, token_data: dict = Depends(JWTBearer())) -> bool:
    json_ = await request.json()
    if 'new_password' not in json_:
        return False
    new_password = json_['new_password']
    if change_user_password(token_data['user_id'], new_password):
        log.info(f"user [{token_data['username']}] change password.")
        return True
    return False

def check_otp_user_exists(username: str) -> bool:
    user = Otp.find_one({'username': username})
    return True if user else False

def insert_otp_user(payload: OtpBaseSchema) -> None:
    payload.created_at = get_now()
    payload.updated_at = payload.created_at
    Otp.insert_one(payload.dict())

@router.post("/otp/generate", tags=["OTP"])
async def generate_otp_user(payload: OtpRequestSchema) -> Union[dict, bool]:
    payload.username = payload.username.lower()
    otp_base32 = pyotp.random_base32()
    ref_number = str(otp_base32)[0:6]
    t = pyotp.TOTP(otp_base32, interval=300)
    otp = t.now()
    updated_user = Otp.find_one_and_update(
        {'username': payload.username},
        {'$set': {
            'otp_base32': otp_base32,
            'otp_enable': True,
            'otp_verified': False,
            'updated_at': get_now()
        }},
        return_document=ReturnDocument.AFTER
    )
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this username: {payload.username} found.')
    
    return email_otp(payload.username, otp, ref_number)

@router.post("/otp/verify", tags=["OTP"])
async def verify_otp(payload: OtpRequestSchema) -> Union[dict, bool]:
    user = Otp.find_one({'username': payload.username})
    if not user.get("otp_enable"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='OTP is not enable')
    totp = pyotp.TOTP(user.get("otp_base32"), interval=300)
    if not totp.verify(payload.token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Token is invalid')
    updated_user = Otp.find_one_and_update(
        {'username': payload.username},
        {'$set': {
            'otp_enable': False,
            'otp_verified': True,
            'otp_base32': None,
            'updated_at': get_now()
        }},
        return_document=ReturnDocument.AFTER
    )
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with this username: {payload.username} found.")
    
    user_id, user_group = check_authenticate(payload.username, payload.password)
    if user_id and user_group:
        access_token = create_access_token(user_id, user_group, payload.username)
        refresh_token = create_refresh_token(user_id, user_group, payload.username)
        log.info(f"[{payload.username}] login.")
        return {"access_token": access_token, "refresh_token": refresh_token}
    
@router.post("/user/check", tags=['user'])
async def check_user(request: Request):
    json_ = await request.json()
    return check_duplicate_user(json_['username'])

@router.post("/sign/contract", tags=['signature'])
def sign_contract(request: dict = Body(...)):
    try:
        action = request['action'] if 'action' in request else 'contractor'
        log.info(f"Sign document request for {request['doc_id']} with contractor {request['contractor_id']} ({action})")
        document = sign_document(request, action)
        return document if document else False
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ไม่สามารถลงนามสัญญาอิเล็กทรอนิกส์ได้")
    
@router.post("/sign/internal", tags=['signature'])
def sign_internal_document(request: dict = Body(...)):
    try:
        action = 'employee'
        log.info(f"Sign document request for {request['doc_id']} with employee {request['employee_id']} ({action})")
        document = sign_document(request, action)
        return document if document else False
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ไม่สามารถลงนามอิเล็กทรอนิกส์")

@router.get("/user/certificate/revoke")
def revoke_certificate(token_data: dict = Depends(JWTBearer())):
    try:
        user_id = token_data['user_id']
        revoke = revoke_contract(user_id)
        if revoke:
            log.info(f"Employee User Id = [{user_id}] revoke certificate complete!")
        else:
            log.info(f"Employee User Id = [{user_id}] revoke certificate failure!")
        return revoke
    except Exception as e:
        log.exception("Cannot Revoke Employee Certificate")
        return False

@router.get("/user/certificate/renew")
def renew_certificate(token_data: dict = Depends(JWTBearer())):
    try:
        user_id = token_data['user_id']
        renew = renew_contract(user_id)
        if renew:
            log.info(f"Employee User Id = [{user_id}] renew certificate complete!")
        else:
            log.info(f"Employee User Id = [{user_id}] renew certificate failure!")
        return renew
    except Exception as e:
        log.exception("Cannot Renew Employee Certificate")
        return False

app.include_router(router)
