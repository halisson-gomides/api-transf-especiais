from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedPlanoTrabalhoEspecialResponse
from datetime import date
from typing import Optional, Literal
from appconfig import Settings
from src.cache import cache

pt_router = APIRouter(tags=["Plano de Trabalho Especial"])
config = Settings()


@pt_router.get("/plano_trabalho_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Planos de Trabalho Especiais.",
                response_description="Lista Paginada de Planos de Trabalho Especiais",
                response_model=PaginatedPlanoTrabalhoEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_plano_trabalho_especial(
    id_plano_trabalho: Optional[int] = Query(None, description="Identificador Único do Plano de Trabalho"),
    situacao_plano_trabalho: Optional[str] = Query(None, description="Situação do Plano de Trabalho"),
    ind_orcamento_proprio_plano_trabalho: Literal["Sim", "Não"] = Query(None, description="Indicador de Orçamento Próprio (Sim|Não)"),
    data_inicio_execucao_plano_trabalho: Optional[str] = Query(None, description="Data de início da execução do Plano de Trabalho"),
    data_fim_execucao_plano_trabalho: Optional[str] = Query(None, description="Data de encerramento do Plano de Trabalho"),
    prazo_execucao_meses_plano_trabalho: Optional[int] = Query(None, description="Prazo de execução do Plano de Trabalho (em meses)"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação correspondente"),
    classificacao_orcamentaria_pt: Optional[str] = Query(None, description="Classificação Orçamentária do Plano de Trabalho"),
    ind_justificativa_prorrogacao_atraso_pt: Optional[bool] = Query(None, description="Indicador de Atraso no Plano de Trabalho"),
    ind_justificativa_prorrogacao_paralizacao_pt: Optional[bool] = Query(None, description="Indicador de Paralização no Plano de Trabalho"),
    justificativa_prorrogacao_pt: Optional[str] = Query(None, description="Identificador Único do Plano de Trabalho"),
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
        query = select(models.PlanoTrabalhoEspecial).where(
            and_(
               models.PlanoTrabalhoEspecial.id_plano_trabalho == id_plano_trabalho if id_plano_trabalho else True,
               models.PlanoTrabalhoEspecial.situacao_plano_trabalho.ilike(f"%{situacao_plano_trabalho}%") if situacao_plano_trabalho else True,
               models.PlanoTrabalhoEspecial.ind_orcamento_proprio_plano_trabalho == ind_orcamento_proprio_plano_trabalho if ind_orcamento_proprio_plano_trabalho else True,
               cast(models.PlanoTrabalhoEspecial.data_inicio_execucao_plano_trabalho, Date) == date.fromisoformat(data_inicio_execucao_plano_trabalho) if data_inicio_execucao_plano_trabalho else True,
               cast(models.PlanoTrabalhoEspecial.data_fim_execucao_plano_trabalho, Date) == date.fromisoformat(data_fim_execucao_plano_trabalho) if data_fim_execucao_plano_trabalho else True,
               models.PlanoTrabalhoEspecial.prazo_execucao_meses_plano_trabalho == prazo_execucao_meses_plano_trabalho if prazo_execucao_meses_plano_trabalho else True,
               models.PlanoTrabalhoEspecial.id_plano_acao == id_plano_acao if id_plano_acao else True,
               models.PlanoTrabalhoEspecial.classificacao_orcamentaria_pt.ilike(f"%{classificacao_orcamentaria_pt}%") if classificacao_orcamentaria_pt else True,
               models.PlanoTrabalhoEspecial.ind_justificativa_prorrogacao_atraso_pt == ind_justificativa_prorrogacao_atraso_pt if ind_justificativa_prorrogacao_atraso_pt is not None else True,
               models.PlanoTrabalhoEspecial.ind_justificativa_prorrogacao_paralizacao_pt == ind_justificativa_prorrogacao_paralizacao_pt if ind_justificativa_prorrogacao_paralizacao_pt is not None else True,
               models.PlanoTrabalhoEspecial.justificativa_prorrogacao_pt.ilike(f"%{justificativa_prorrogacao_pt}%") if justificativa_prorrogacao_pt else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedPlanoTrabalhoEspecialResponse, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro ao consultar Plano de Trabalho: {e.__repr__()}")