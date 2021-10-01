from fastapi import APIRouter


from apis.version1 import route_user
from apis.version1 import route_device
from apis.version1 import route_group
from apis.version1 import route_association
from apis.version1 import route_login
from apis.version1 import route_role
from apis.version1 import route_userrole


api_router = APIRouter()


api_router.include_router(route_user.router, prefix="/user", tags=['users'])
api_router.include_router(
    route_device.router, prefix="/device", tags=['devices'])
api_router.include_router(route_group.router, prefix="/devicegroup", tags=['devicegroup'])
api_router.include_router(route_association.router, prefix="/group-device", tags=['group-device-relation'])
api_router.include_router(route_login.router, prefix="/login", tags=['/login'])
api_router.include_router(route_role.router, prefix="/role", tags=['/roles'])
api_router.include_router(route_userrole.router, prefix="/user_role", tags=['/userrole'])
