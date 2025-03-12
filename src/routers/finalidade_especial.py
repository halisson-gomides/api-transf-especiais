from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedFinalidadeEspecialResponse
from datetime import date
from typing import Optional
from src.cache import cache

fe_router = APIRouter(tags=["Finalidade Especial"])



@fe_router.get("/finalidade_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Finalidades Especiais.",
                response_description="Lista Paginada de Finalidade Especial",
                response_model=PaginatedFinalidadeEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_finalidade_especial(
    id_executor: Optional[int] = Query(None, description="Identificador Único do Executor Especial"),
    cd_area_politica_publica_tipo_pt: Optional[int] = Query(None, description="Código do tipo de política pública da Finalidade Plano de Trabalho Especial"),
    area_politica_publica_tipo_pt: Optional[str] = Query(None, description="Descrição do tipo de política pública da Finalidade do Plano de Trabalho Especial"),
    cd_area_politica_publica_pt: Optional[int] = Query(None, description="Código da área da política pública da Finalidade do Plano de Trabalho Especial"),
    area_politica_publica_pt: Optional[str] = Query(None, description="Descrição da área da política pública da Finalidade do Plano de Trabalho Especial"),
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
        query = select(models.FinalidadeEspecial).where(
            and_(
                models.FinalidadeEspecial.id_executor == id_executor if id_executor else True,
                models.FinalidadeEspecial.cd_area_politica_publica_tipo_pt == cd_area_politica_publica_tipo_pt if cd_area_politica_publica_tipo_pt else True,
                models.FinalidadeEspecial.area_politica_publica_tipo_pt.ilike(f"%{area_politica_publica_tipo_pt}%") if area_politica_publica_tipo_pt else True,
                models.FinalidadeEspecial.cd_area_politica_publica_pt == cd_area_politica_publica_pt if cd_area_politica_publica_pt else True,
                models.FinalidadeEspecial.area_politica_publica_pt.ilike(f"%{area_politica_publica_pt}%") if area_politica_publica_pt else True
            )
        )
        # print(query.compile(compile_kwargs={"literal_binds":True}))
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedResponseTemplate, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=config.ERROR_MESSAGE_INTERNAL)