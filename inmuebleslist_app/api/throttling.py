from rest_framework.throttling import UserRateThrottle


class ComentarioCreateThrottle(UserRateThrottle):
    scope = "comentario-create"


class ComentarioListThrottle(UserRateThrottle):
    scope = "comentario-list"
