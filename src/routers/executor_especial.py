from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedExecutorEspecialResponse
from datetime import date
from typing import Optional
from src.cache import cache

ex_router = APIRouter(tags=["Executor Especial"])



@ex_router.get("/executor_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Executores Especiais.",
                response_description="Lista Paginada de Executor Especial",
                response_model=PaginatedExecutorEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_executor_especial(
    id_executor: Optional[int] = Query(None, description="Identificador Único do Executor Especial"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação correspondente"),
    cnpj_executor: Optional[str] = Query(None, description="CNPJ do Executor Especial"),
    nome_executor: Optional[str] = Query(None, description="Nome do Executor Especial"),
    objeto_executor: Optional[str] = Query(None, description="Objeto do Executor Especial"),
    vl_custeio_executor: Optional[float] = Query(None, description="Valor de Custeio do Executor Especial", ge=0),
    vl_investimento_executor: Optional[float] = Query(None, description="Valor de Investimento do Executor Especial", ge=0),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params = locals().copy()
    params_list = list(params.keys())[:-3]    
    
    if all([params[_name] is None for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nenhum parâmetro de consulta foi informado.")
    
    try:
        query = select(models.ExecutorEspecial).where(
            and_(
                models.ExecutorEspecial.id_executor == id_executor if id_executor else True,
                models.ExecutorEspecial.id_plano_acao == id_plano_acao if id_plano_acao else True,
                models.ExecutorEspecial.cnpj_executor.ilike(f"%{cnpj_executor}%") if cnpj_executor else True,
                models.ExecutorEspecial.nome_executor.ilike(f"%{nome_executor}%") if nome_executor else True,
                models.ExecutorEspecial.objeto_executor.ilike(f"%{objeto_executor}%") if objeto_executor else True,
                models.ExecutorEspecial.vl_custeio_executor == vl_custeio_executor if vl_custeio_executor else True,
                models.ExecutorEspecial.vl_investimento_executor == vl_investimento_executor if vl_investimento_executor else True
            )
        )        
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)