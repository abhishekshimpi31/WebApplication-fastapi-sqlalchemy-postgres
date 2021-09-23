from passlib.context import CryptContext


pwt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Hasher():

    @staticmethod
    def verify_passwd(plain_passwd, hash_passwd):
        return pwt_context.verify(plain_passwd, hash_passwd)

    @staticmethod
    def get_passwd_hash(plain_passwd):
        return pwt_context.hash(plain_passwd)
