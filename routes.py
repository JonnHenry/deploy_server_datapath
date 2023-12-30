from fastapi import APIRouter
from controllers.stroke_controller import router as ml_router


router_  = APIRouter()

# Incluir el path de los routes
router_.include_router(ml_router)