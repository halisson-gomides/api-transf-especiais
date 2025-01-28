from contextlib import asynccontextmanager
from fastapi import FastAPI
import orjson
from fastapi.responses import RedirectResponse, ORJSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import logging
from appconfig import Settings

from src.database import Database

# Importando Rotas
from src.routers.programa_especial import prg_router
from src.routers.plano_acao_especial import pa_router
from src.routers.empenho_especial import em_router
from src.routers.documento_habil import dh_router
from src.routers.ordem_pagamento_especial import op_router
from src.routers.historico_pagamento_especial import hist_router

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the database instance
db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load before the app starts
    logger.info("Iniciando aplicação...")
    try:
        await db.init_db()
        logger.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        raise
    yield
    # load after the app has finished
    # ...
    

settings = Settings()
app = FastAPI(lifespan=lifespan, 
              docs_url=None, 
              title=settings.APP_NAME, 
              description=settings.APP_DESCRIPTION,
              openapi_tags=settings.APP_TAGS,
              default_response_class=ORJSONResponse)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluindo Rotas
app.include_router(prg_router)
app.include_router(pa_router)
app.include_router(em_router)
app.include_router(dh_router)
app.include_router(op_router)
app.include_router(hist_router)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.APP_NAME + " - Documentação",        
        swagger_favicon_url="/static/icon.jpg"
    )


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')