# app/odoo/contractor.py
from app.helpers.odoo import Odoo
from app.odoo.certificate import create_pfx

from typing import Union
from app.model import UserRegister, UserEdit

odoo = Odoo()

def get_contractor_detail(user_id: int) -> Union[dict, bool]:
    user = odoo.search_read('depa_contract', [
        ['user_id', '=', user_id]
    ])
    return user[0] if user else False

def get_contractor_detail_from_id(contractor_id: int) -> Union[dict, bool]:
    user = odoo.search_read('depa_contract', [
        ['id', '=', contractor_id]
    ])
    return user[0] if user else False

def create_contractor_res_user(user_data: UserRegister) -> Union[int, bool]:
    create = odoo.create('res.users', {
        'name': user_data.name.strip(),
        'login': user_data.username,
        'image': False,
        'lang': 'th_TH',
        'tz': 'Asia/Bangkok',
        'odoobot_state': 'onboarding_emoji',
        'new_password': user_data.password,
        'sel_groups_1_9_10': 9
    })
    return create if create else False

def get_partner_id(user_id: int) -> Union[int, bool]:
    res_user = odoo.search_read('res.users', [
        ['id', '=', user_id]
    ], {
        'fields': ['partner_id']
    })
    return res_user[0]['partner_id'] if res_user else False

def update_partner_email(partner_id: int, user_data: UserRegister) -> None:
    odoo.write('res.partner', partner_id, {
        'email': user_data.email
    })

def create_contractor(user_data: UserRegister, res_user_id: int, encoded_image: str, cad_password: str, attachment_id: int) -> bool:
    create = odoo.create('depa_contract', {
        'name': user_data.name.strip(),
        'company': user_data.company,
        'email': user_data.email,
        'user_id': res_user_id,
        'cad_password': cad_password,
        'sign_img': encoded_image,
        'certificate_file': [(6, 0, [attachment_id])]
    })
    return True if create else False

def upload_attachment(file_name: str, file_base64: str) -> Union[int, bool]:
    try:
        create = odoo.create('ir.attachment', {
            'name': file_name,
            'datas_fname': file_name,
            'datas': file_base64
        })
        return create if create else False
    except:
        return False

def register_contractor(user_data: UserRegister, encoded_image: str) -> bool:
    file_name = "certificate.p12"
    try:
        p12_base64, p12_password = create_pfx(file_name, user_data.name, user_data.email)
        if p12_base64 and p12_password:
            attachment_id = upload_attachment(file_name, p12_base64)
            res_user = create_contractor_res_user(user_data)
            partner_id = get_partner_id(res_user)
            if res_user and partner_id:
                update_partner_email(partner_id[0], user_data)
                contractor = create_contractor(user_data, res_user, encoded_image, p12_password, attachment_id)
                if contractor:
                    return True
            return False
    except:
        return False
    
def get_contractor_id(user_id: int) -> Union[int, bool]:
    depa_contract_id = odoo.search('depa_contract', [
        ['user_id', '=', user_id]
    ])
    return depa_contract_id[0] if depa_contract_id else False

def update_contractor(user_id: int, user_data: UserEdit, encoded_image: str = None) -> bool:
    contractor_id = get_contractor_id(user_id)
    if user_id:
        update_data = {
            'name': user_data.name.strip(),
            'company': user_data.company,
            'email': user_data.email,
		}
        if encoded_image is not None:
            update_data['sign_img'] = encoded_image
        update = odoo.write('depa_contract', contractor_id, update_data)
    return True if update else False

def revoke_contract(user_id: int) -> bool:
    contractor_id = get_contractor_id(user_id)
    if contractor_id:
        update_data = {
            'active_contract': False,
            'cad_password': False,
            'certificate_file': [(6, 0, [])]
        }
        update = odoo.write('depa_contract', contractor_id, update_data)
        return True if update else False
    return False

def renew_contract(user_id: int) -> bool:
    contractor = get_contractor_detail(user_id)
    if contractor:
        file_name = "certificate.p12"
        try:
            p12_base64, p12_password = create_pfx(file_name, contractor.get('name'), contractor.get('email'))
            if p12_base64 and p12_password:
                attachment_id = upload_attachment(file_name, p12_base64)
                update_data = {
                    'active_contract': True,
                    'cad_password': p12_password,
                    'certificate_file': [(6, 0, [attachment_id])]
                }
                update = odoo.write('depa_contract', contractor.get('id'), update_data)
            return True if update else False
        except:
            return False
    return False