from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedRelatorioGestaoEspecialResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

rg_router = APIRouter(tags=["Relatório de Gestão Especial"])
config = Settings()

@rg_router.get("/relatorio_gestao_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada de dados de Relatórios de Gestão Especial.",
                response_description="Lista Paginada com dados de Relatórios de Gestão Especial",
                response_model=PaginatedRelatorioGestaoEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_relatorio_gestao_especial(
    id_relatorio_gestao : Optional[int] = Query(None, description="Identificador Único do Relatório de Gestão"),
    situacao_relatorio_gestao : Optional[str] = Query(None, description="Situação do Relatório de Gestão"),
    parecer_relatorio_gestao : Optional[str] = Query(None, description="Parecer do Relatório de Gestão"),
    id_plano_acao : Optional[int] = Query(None, description="Identificador Único do Plano de Ação (PA)"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):

    params = locals().copy()
    params_list = list(params.keys())[:-3]    
    
    if not any([params[_name] for _name in params_list]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nenhum parâmetro de consulta foi informado.")
    
    try:
        query = select(models.RelatorioGestaoEspecial).where(
            and_(
                models.RelatorioGestaoEspecial.id_relatorio_gestao == id_relatorio_gestao if id_relatorio_gestao else True,
                models.RelatorioGestaoEspecial.situacao_relatorio_gestao.ilike(f"%{situacao_relatorio_gestao}%") if situacao_relatorio_gestao else True,
                models.RelatorioGestaoEspecial.parecer_relatorio_gestao.ilike(f"%{parecer_relatorio_gestao}%") if parecer_relatorio_gestao else True,
                models.RelatorioGestaoEspecial.id_plano_acao == id_plano_acao if id_plano_acao else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedRelatorioGestaoEspecialResponse, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro ao consultar Relatório de Gestão: {e.__repr__()}")