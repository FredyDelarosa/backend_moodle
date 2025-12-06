from fastapi import APIRouter
from routes.academy_programas import router as programas_router
from routes.academy_cuatrimestres import router as cuatrimestres_router
from routes.academy_asignaturas import router as asignaturas_router
from routes.academy_docentes import router as docentes_router
from routes.academy_docente_asignatura import router as docente_asignatura_router
from routes.academy_alumnos import router as alumnos_router
from routes.academy_grupos import router as grupos_router

router = APIRouter(prefix="/api")

router.include_router(programas_router)
router.include_router(cuatrimestres_router)
router.include_router(asignaturas_router)
router.include_router(docentes_router)
router.include_router(docente_asignatura_router)
router.include_router(alumnos_router)
router.include_router(grupos_router)
