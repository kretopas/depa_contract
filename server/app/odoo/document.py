# app/odoo/document.py
from app.helpers.logger import log
from app.helpers.odoo import Odoo

import requests
import base64
import json
from decouple import config
from typing import Union

odoo = Odoo()

CONVERT_API = config("DOCX_TO_PDF")
EXCEPT_CONDITION = ['cancel', 'draft', 'done']
COMPLETE_EXCEPT_CONDITION = ['cancel', 'draft']

def get_docx_from_document(document_id: int) -> Union[str, bool]:
    try:
        document = odoo.search_read('document.internal.main', [
            ['id', '=', document_id]
        ], {
            'fields': ['file_for_signature']
        })
        return document[0]['file_for_signature'] if document else False
    except:
        log.exception("[Document] get_docx_from_document")
        return False

def get_preview_document(document_id: int) -> Union[str, bool]:
    try:
        file_base64 = base64.b64decode(get_docx_from_document(document_id))
        file_name = "docx_file.docx"
        action = {"docxFile": (file_name, file_base64)}
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        resp = requests.post(CONVERT_API, files=action, headers=headers)
        response_code = resp.status_code
        response_data = resp.text
        if response_code == 200:
            json_data = json.loads(response_data)
            data_base64 = json_data['base64']
            return data_base64
        return False
    except:
        log.exception("[Document] get_preview_document")
        return False

def check_contract_is_not_approved(doc_id: int, user_id: int) -> bool:
    try:
        data = odoo.search('depa_contract_lines', [
            ['contract_approval_lines_id', '=', doc_id],
            ['contract_id.user_id', '=', user_id],
            ['status', '=', 0]
        ])
        return True if data else False
    except:
        log.exception("[Document] check_contract_is_not_approved")
        return False
    
def check_contract_is_approved(doc_id: int, user_id: int) -> bool:
    try:
        data = odoo.search('depa_contract_lines', [
            ['contract_approval_lines_id', '=', doc_id],
            ['contract_id.user_id', '=', user_id],
            ['status', '=', 1]
        ])
        return True if data else False
    except:
        log.exception("[Document] check_contract_is_approved")
        return False

def get_contractor_waiting_documents(user_id: int) -> Union[list, bool]:
    try:
        data = odoo.search_read('document.internal.main', [
            ['contract_approval_lines_ids.contract_id.user_id', '=', user_id],
            ['state', 'not in', EXCEPT_CONDITION]
        ], {
            'fields': ['id', 'name', 'subject'],
            'order': 'id desc'
        })
        if data:
            available_doc = [doc for doc in data if check_contract_is_not_approved(doc['id'], user_id)]
            return available_doc if len(available_doc) > 0 else False
        return False
    except:
        log.exception("[Document] get_contractor_waiting_documents")
        return False
    
def get_contractor_signed_documents(user_id: int) -> Union[list, bool]:
    try:
        data = odoo.search_read('document.internal.main', [
            ['contract_approval_lines_ids.contract_id.user_id', '=', user_id],
            ['state', 'not in', COMPLETE_EXCEPT_CONDITION]
        ], {
            'fields': ['id', 'name', 'subject'],
            'order': 'id desc'
        })
        if data:
            available_doc = [doc for doc in data if check_contract_is_approved(doc['id'], user_id)]
            return available_doc if len(available_doc) > 0 else False
        return False
    except:
        log.exception("[Document] get_contractor_signed_documents")
        return False
    
def get_contractor_document_detail(user_id: int, document_id: int, waiting: bool = True) -> Union[dict, bool]:
    try:
        condition = [['id', '=', document_id]]
        if waiting:
            condition.append(['state', 'not in', EXCEPT_CONDITION])
        else:
            condition.append(['state', 'not in', COMPLETE_EXCEPT_CONDITION])
        document = odoo.search_read('document.internal.main', condition, {
            'fields': ['id', 'name', 'subject']
        })[0]
        if document and (
            check_contract_is_not_approved(document['id'], user_id) if
            waiting else
            check_contract_is_approved(document['id'], user_id)
        ):
            return document
        return False
    except:
        log.exception("[Dcoument] get_contractor_document_detail")
        return False