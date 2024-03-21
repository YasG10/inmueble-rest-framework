from django.urls import path, include
from rest_framework import routers
from inmuebleslist_app.api.views import (
    InmueblesListAV,
    InmuebleDetallesAV,
    EmpresaAV,
    EmpresaDetalleAV,
    ComentariosList,
    ComentariosDetail,
    ComentariosCreate,
    EmpresaVS,
    UsuarioComentario,
    InmuebleList,
)

router = routers.DefaultRouter()
router.register("empresa", EmpresaVS, basename="empresa")

urlpatterns = [
    path("inmueble/", InmueblesListAV.as_view(), name="inmueble"),
    path("inmueble/list/", InmuebleList.as_view(), name="inmueble-list"),
    path("inmueble/<int:pk>", InmuebleDetallesAV.as_view(), name="inmueble-detail "),
    path("", include(router.urls)),
    # path("empresa/", EmpresaAV.as_view(), name="empresa"),
    # path("empresa/<int:pk>", EmpresaDetalleAV.as_view(), name="empresa-detail"),
    path(
        "inmueble/<int:pk>/comentario-create/",
        ComentariosCreate.as_view(),
        name="comentario-create",
    ),
    path(
        "inmueble/<int:pk>/comentario/",
        ComentariosList.as_view(),
        name="comentario-list",
    ),
    path(
        "inmueble/comentario/<int:pk>",
        ComentariosDetail.as_view(),
        name="comentario-detail",
    ),
    #path(
    #    "inmueble/comentarios/<str:username>/",
    #    UsuarioComentario.as_view(),
    #    name="usuario-comentario-detail",
    #),
    path(
        "inmueble/comentarios/",
        UsuarioComentario.as_view(),
        name="usuario-comentario-detail",
    ),
]
