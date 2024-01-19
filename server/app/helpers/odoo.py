# app/helpers/odoo.py

import xmlrpc.client
from decouple import config
from typing import Union

class Odoo():
    def __init__(self) -> None:
        """
        สร้่างคลาส Odoo สำหรับการเชื่อมต่อกับ odoo-api ของ depa
        """

        url = config("ODOO_URL")
        db = config("ODOO_DB")
        username = config("ODOO_USERNAME")
        password = config("ODOO_PASSWORD")

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        self.__db = db
        self.__uid = uid
        self.__password = password
        self.identity = (db, uid, password)

    def create(self, model:str, data: list) -> Union[int, bool]:
        try:
            create_id = self.models.execute_kw(self.__db, self.__uid, self.__password,
                model, 'create',
                [data]
            )
            return create_id
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def write(self, model: str, id: int, data: dict) -> bool:
        try:
            self.models.execute_kw(self.__db, self.__uid, self.__password,
                model, 'write',
                [[id], data]
            )
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def search(self, model: str, condition: list) -> Union[list, bool]:
        try:
            data = self.models.execute_kw(self.__db, self.__uid, self.__password,
                model, 'search',
                [condition]
            )
            return data
        except Exception as e:
            print(f"Error: {e}")
            return False

    def search_read(self, model: str, condition: list, options: dict={}) -> Union[list, bool]:
        try:
            data = self.models.execute_kw(self.__db, self.__uid, self.__password,
                model, 'search_read',
                [condition],
                options
            )
            return data
        except Exception as e:
            print(f"Error: {e}")
            return False

    def unlink(self, model: str, id: int) -> None:
        try:
            self.models.execute_kw(self.__db, self.__uid, self.__password,
                model, 'unlink',
                [id]
            )
        except Exception as e:
            print(f"Error: {e}")
        
    def custom_function(self, model: str, function: str, id: int) -> None:
        try:
            self.models.execute_kw(self.__db, self.__uid, self.__password,
                model, function,
                [[id]]
            )
        except Exception as e:
            print(f"Error: {e}")