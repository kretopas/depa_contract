# app/odoo/signature.py
from app.helpers.odoo import Odoo
from app.helpers.logger import log
from app.odoo.contractor import get_contractor_detail_from_id
from app.odoo.employee import get_employee_detail_from_user_id

import base64
import os
import uuid
from datetime import datetime, date, timezone
from decouple import config
from fastapi import UploadFile
from os.path import join as pj
from pyhanko import stamp
from pyhanko.pdf_utils import images
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields, signers
from typing import Union

TEMP_FOLDER = pj(os.path.dirname(os.path.abspath(__file__)), "temp")
SIGNATURE_LOCATION = pj(TEMP_FOLDER, "signature.png")
FILE_EXCEPTIONS = [".gitignore"]

odoo = Odoo()

def get_encoded_signature(sing_img: UploadFile) -> Union[str, bool]:
    try:
        with open(SIGNATURE_LOCATION, "wb") as f:
            f.write(sing_img.file.read())
            f.close()
        with open(SIGNATURE_LOCATION, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode('utf-8')
    except:
        return False
    finally:
        os.remove(SIGNATURE_LOCATION)
        return encoded_image

def get_contract_line(user_id: int, document_id: int) -> Union[int, bool]:
    contract_line = odoo.search('depa_contract_lines', [
        ['contract_id.user_id', '=', user_id],
        ['contract_approval_lines_id', '=', document_id]
    ])
    return contract_line[0] if contract_line else False

def sign_contractor_document(user_id: int, document_id: int) -> bool:
    try:
        contract_line = get_contract_line(user_id, document_id)
        if contract_line:
            odoo.write('depa_contract_lines', contract_line, {
                'status': '1',
                'approved_date': datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            })
        return True
    except:
        return False
    
def download_pfx(pfx_id: int, file_path: str) -> bool:
    try:
        #log.info("Start download PFX File...")
        data = odoo.search_read('ir.attachment', [
            ['id', '=', pfx_id]
        ], {
            'fields': ['datas']
        })
        if data:
            data = data[0]
            data_base64 = data['datas']
            with open(file_path, 'wb') as p12_file:
                file_content = base64.b64decode(data_base64)
                p12_file.write(file_content)
                #log.info("Download PFX File successfull")
                return True
        return False
    except:
        log.exception("Download PFX fail")
        return False

def download_signature(signature_base64: str, file_path: str) -> bool:
    try:
        #log.info("Start download Signature Image...")
        with open(file_path, 'wb') as signature_file:
            file_content = base64.b64decode(signature_base64)
            signature_file.write(file_content)
            #log.info("Download Signature Image successfull")
        return True
    except:
        log.exception("Download Signature Image fail")
        return False

def download_document(document_base64: str, file_path: str) -> bool:
    try:
        #log.info("Start download Document PDF...")
        with open(file_path, 'wb') as document_file:
            file_content = base64.b64decode(document_base64)
            document_file.write(file_content)
            #log.info("Download Document PDF successfull")
        return True
    except:
        log.exception("Download Document PDF fail")
        return False

def remove_temporary() -> None:
    for filename in os.listdir(TEMP_FOLDER):
        if filename in FILE_EXCEPTIONS:
            continue
        file_path = pj(TEMP_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except:
            log.exception(f"delete {filename} fail")

def sign_document(data: dict, action: str = "contractor") -> Union[str, bool]:
    if action == "contractor":
        approver = get_contractor_detail_from_id(data['contractor_id'])
    elif action == "employee":
        approver = get_employee_detail_from_user_id(data['employee_id'])
    
    pfx_id = approver['certificate_file'][0]
    pfx_path = pj(TEMP_FOLDER, 'certificate.p12')
    signature_base64 = approver['sign_img']
    signature_path = pj(TEMP_FOLDER, 'signature.png')
    document_base64 = data['pdf_file']
    document_path = pj(TEMP_FOLDER, 'document.pdf')

    try:
        if all([
            download_pfx(pfx_id, pfx_path),
            download_signature(signature_base64, signature_path),
            download_document(document_base64, document_path)
        ]):
            output_path = pj(TEMP_FOLDER, 'document-sign.pdf')
            #log.info("Start Signing Document...")
            signer = signers.SimpleSigner.load_pkcs12(
                pfx_file=pfx_path,
                passphrase=approver['cad_password'].encode('utf-8')
            )
            random_uuid = uuid.uuid4().hex
            with open(document_path, 'rb') as inf:
                w = IncrementalPdfFileWriter(inf, strict=False)
                x = data['x']
                y = data['y'] if action == 'contract' else (data['y'] - 20)
                adj_y = 13 + ((abs(210 - y))/6.17) if action == 'employee' else 0
                y = y - adj_y
                fields.append_signature_field(
                    w, sig_field_spec=fields.SigFieldSpec(
                        random_uuid,
                        box=(x, y, x+100, y+50),
                        on_page=(data['page'] - 1)
                    )
                )
                meta = signers.PdfSignatureMetadata(field_name=random_uuid)
                pdf_signer = signers.PdfSigner(
                    meta, signer = signer, stamp_style= stamp.TextStampStyle(
                        stamp_text='',
                        border_width=0,
                        background_opacity=1,
                        background=images.PdfImage(signature_path)
                    )
                )
                with open(output_path, 'wb') as outf:
                    pdf_signer.sign_pdf(w, output=outf)
                with open(output_path, 'rb') as signed_file:
                    signed_pdf = signed_file.read()
                    signed_base64 = base64.b64encode(signed_pdf).decode('utf-8')
                    #log.info("Document Sign successfull")
                    return signed_base64.replace('"', '')
        return False
    except:
        log.exception("Signing Document fail")
        return False
    finally:
        log.info("====================================================")
        remove_temporary()