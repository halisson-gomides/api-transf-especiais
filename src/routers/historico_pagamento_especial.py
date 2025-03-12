from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedHistoricoPagamentoEspecialResponse
from datetime import date
from typing import Optional
from src.cache import cache

hist_router = APIRouter(tags=["Histórico de Pagamento Especial"])


@hist_router.get("/historico_pagamento_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada do histórico de pagamentos.",
                response_description="Lista Paginada de Histório de Pagamentos",
                response_model=PaginatedHistoricoPagamentoEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_historico_pagamento_especial(
    id_historico_op_ob : Optional[int] = Query(None, description="Identificador Único do Histórico de Pagamento"),
    data_hora_historico_op : Optional[str] = Query(None, description="Data do Histórico de Pagamento<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    historico_situacao_op : Optional[int] = Query(None, description="Código da Situação da Ordem de Pagamento/Bancária"),
    descricao_historico_situacao_op : Optional[str] = Query(None, description="Descrição da Situação da Ordem de Pagamento/Bancária"),
    id_op_ob : Optional[int] = Query(None, description="Identificador Único da Ordem de Pagamento e Ordem Bancária (OP/OB)"),
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
        query = select(models.HistoricoPagamentoEspecial).where(
            and_(
                models.HistoricoPagamentoEspecial.id_historico_op_ob == id_historico_op_ob if id_historico_op_ob else True,
                cast(models.HistoricoPagamentoEspecial.data_hora_historico_op, Date) == date.fromisoformat(data_hora_historico_op) if data_hora_historico_op else True,
                models.HistoricoPagamentoEspecial.historico_situacao_op == historico_situacao_op if historico_situacao_op else True,
                models.HistoricoPagamentoEspecial.descricao_historico_situacao_op.ilike(f"%{descricao_historico_situacao_op}%") if descricao_historico_situacao_op else True,
                models.HistoricoPagamentoEspecial.id_op_ob == id_op_ob if id_op_ob else True
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