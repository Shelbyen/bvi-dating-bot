from . import user_registration, acne_assessment, user_menu
from ..filters.permission_filter import PermissionFilter
from ..middlewares.album_middleware import AlbumMiddleware


user_registration.router.message.filter(PermissionFilter(False))
user_registration.router.message.middleware(AlbumMiddleware())
acne_assessment.router.message.filter(PermissionFilter())
user_menu.router.message.filter(PermissionFilter())

routers = (
    user_registration.router,
    acne_assessment.router,
    user_menu.router
)
