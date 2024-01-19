# app/odoo/certificate.py

import os
import base64
import random
import string
from decouple import config
from typing import Union, Tuple
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from os.path import join as pj

ROOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
KEY_SIZE = config("CERT_KEY_SIZE", cast=int)

def create_temp_key() -> None:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE,
        backend=default_backend()
    )
    with open(pj(ROOT_FOLDER, 'tmp.key'), 'wb') as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

def create_temp_csr(name: str, email: str) -> None:
    with open(pj(ROOT_FOLDER, 'tmp.key'), 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, name),
        x509.NameAttribute(NameOID.COUNTRY_NAME, 'TH'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Bangkok'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, 'Bangkok'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Digital Economy Promotion Agency'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, 'depa'),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, email),
    ])
    csr = x509.CertificateSigningRequestBuilder().subject_name(
        subject
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True,
    ).sign(
        private_key, hashes.SHA256(), default_backend()
    )
    with open(pj(ROOT_FOLDER, 'tmp.csr'), 'wb') as csr_file:
        csr_file.write(csr.public_bytes(serialization.Encoding.PEM))

def create_temp_crt() -> None:
    with open('ca.crt', 'rb') as ca_cert_file, open('ca.key', 'rb') as ca_key_file:
        ca_cert = x509.load_pem_x509_certificate(ca_cert_file.read())
        ca_key = serialization.load_pem_private_key(ca_key_file.read(), password=None, backend=default_backend())
    with open(pj(ROOT_FOLDER, 'tmp.csr'), 'rb') as csr_file:
        csr = x509.load_pem_x509_csr(csr_file.read())
    builder = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        ca_cert.not_valid_before
    ).not_valid_after(
        ca_cert.not_valid_before.replace(year=ca_cert.not_valid_before.year + 10) # set validity to 10 years
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False
    ).add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_cert.public_key()), critical=False
    ).add_extension(
        x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False
        ), critical=True
    ).add_extension(
        x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CODE_SIGNING]), critical=True
    )
    certificate = builder.sign(
        private_key=ca_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )
    with open(pj(ROOT_FOLDER, 'tmp.crt'), 'wb') as cert_file:
        cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))

def convert_psk12_to_base64(p12_file: str) -> str:
    with open(pj(ROOT_FOLDER, p12_file), 'rb') as f:
        p12_bytes = f.read()
    p12_base64 = base64.b64encode(p12_bytes).decode('utf-8')
    return p12_base64

def remove_temp_files():
    for filename in os.listdir(ROOT_FOLDER):
        file_path = pj(ROOT_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {filename}. Reason: {e}")

def generate_password(length):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for i in range(length))
    return password

def create_pfx(output_file: str, name: str, email: str) -> Tuple[Union[str, bool], Union[str, bool]]:
    try:
        create_temp_key()
        create_temp_csr(name, email)
        create_temp_crt()
        with open(pj(ROOT_FOLDER, 'tmp.crt'), 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read())
        with open(pj(ROOT_FOLDER, 'tmp.key'), 'rb') as f:
            key = serialization.load_pem_private_key(f.read(), password=None)
        password = generate_password(64)
        passphrase = password.encode()
        p12 = pkcs12.serialize_key_and_certificates(
            name=b'My PKCS12',
            key=key,
            cert=cert,
            cas=None,
            encryption_algorithm=serialization.BestAvailableEncryption(passphrase)
        )
        with open(pj(ROOT_FOLDER, output_file), 'wb') as f:
            f.write(p12)
        p12_base64 = convert_psk12_to_base64(output_file)
        return p12_base64, password
    except:
        return False, False
    finally:
        remove_temp_files()
