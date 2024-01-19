# app/odoo/employee.py
from app.helpers.odoo import Odoo
from app.odoo.contractor import upload_attachment
from app.odoo.certificate import create_pfx

from typing import Union

odoo = Odoo()

def get_employee_detail(emp_id: int) -> Union[dict, bool]:
	data = odoo.search_read('hr.employee', [
		['id', '=', emp_id]
	], {
		'fields': ['name', 'cad_password', 'certificate_file']
	})
	return data[0] if data else False

def get_employee_detail_from_user_id(user_id: int) -> Union[dict, bool]:
	data = odoo.search_read('hr.employee', [
		['user_id', '=', user_id]
	], {
		'fields': ['name', 'cad_password', 'certificate_file', 'sign_img']
	})
	return data[0] if data else False

def get_employee_from_user_id(user_id: int) -> Union[dict, bool]:
	data = odoo.search_read('hr.employee', [
		['user_id', '=', user_id]
	], {
		'fields': ['name', 'work_email']
	})
	return data[0] if data else False

def update_employee(emp_id:int, data: dict) -> bool:
	try:
		update = odoo.write('hr.employee', emp_id, data)
		return update
	except:
		return False
	

def register_employee_certificate(user_id: int) -> bool:
	file_name = "certificate.p12"
	try:
		employee = get_employee_from_user_id(user_id)
		if employee:
			p12_base64, p12_password = create_pfx(file_name, employee['name'], employee['work_email'])
			if p12_base64 and p12_password:
				attachment_id = upload_attachment(file_name, p12_base64)
				update_data = update_employee(employee['id'], {
					"cad_password": p12_password,
					"certificate_file": [(6, 0, [attachment_id])]
				})
				return update_data
		return False
	except:
		return False