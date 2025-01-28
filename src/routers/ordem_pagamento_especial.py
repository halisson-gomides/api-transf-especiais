from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedOrdemPagamentoOrdemBancariaEspecialResponse
from datetime import date
from typing import Optional
from appconfig import Settings

op_router = APIRouter(tags=["Ordem de pagamento e Ordem bancária Especial"])
config = Settings()

@op_router.get("/ordem_pagamento_ordem_bancaria_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Ordens de Pagamento e Ordens Bancárias Especiais.",
                response_description="Lista Paginada de Ordens de Pagamento e Ordens Bancárias Especiais",
                response_model=PaginatedOrdemPagamentoOrdemBancariaEspecialResponse
                )
async def consulta_ordem_pagamento_ordem_bancaria_especial(
    id_op_ob : Optional[int] = Query(None, description="Identificador Único da Ordem de Pagamento e Ordem Bancária (OP/OB)"),
    data_emissao_op : Optional[str] = Query(None, description="Data de Emissão da Ordem de Pagamento (OP)<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    numero_ordem_pagamento : Optional[str] = Query(None, description="Número da Ordem de Pagamento, no formato AAAAOPNNNNNN<br/>Ex.: “2020OP146800”", min_length=12, examples=["2020OP146800"]),
    vinculacao_op : Optional[int] = Query(None, description="Código da Vinculação da Ordem de Pagamento no SIAFI (Padrão: 405)"),
    situacao_op : Optional[int] = Query(None, description="Código da Situação da Ordem de Pagamento/Bancária"),
    descricao_situacao_op : Optional[str] = Query(None, description="Descrição da Situação da Ordem de Pagamento/Bancária"),
    data_situacao_op : Optional[str] = Query(None, description="Data da Situação da Ordem de Pagamento/Bancária<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    data_emissao_ob : Optional[str] = Query(None, description="Data de Emissão da Ordem Bancária (OB)<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    numero_ordem_bancaria : Optional[str] = Query(None, description="Número da Ordem Bancária, no formato AAAAOBNNNNNN<br/>Ex.: “2020OB146800”", min_length=12, examples=["2020OB146800"]),
    numero_ordem_lancamento : Optional[str] = Query(None, description="Número da Nota de Lançamento no sistema, no formato AAAANSNNNNNN<br/>Ex.: “2020NS146800”", min_length=12, examples=["2020NS146800"]),
    data_assinatura_ordenador_despesa_ob : Optional[str] = Query(None, description="Data da Assinatura do Ordenador de Despesa<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    data_assinatura_gestor_financeiro_ob : Optional[str] = Query(None, description="Data da Assinatura do Gestor Financeiro<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    id_dh : Optional[int] = Query(None, description="Identificador Único do Documento Hábil (DH)"),
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
        query = select(models.OrdemPagamentoOrdemBancariaEspecial).where(
            and_(
                models.OrdemPagamentoOrdemBancariaEspecial.id_op_ob == id_op_ob if id_op_ob else True,
                models.OrdemPagamentoOrdemBancariaEspecial.data_emissao_op == date.fromisoformat(data_emissao_op) if data_emissao_op else True,
                models.OrdemPagamentoOrdemBancariaEspecial.numero_ordem_pagamento == numero_ordem_pagamento if numero_ordem_pagamento else True,
                models.OrdemPagamentoOrdemBancariaEspecial.vinculacao_op == vinculacao_op if vinculacao_op else True,
                models.OrdemPagamentoOrdemBancariaEspecial.situacao_op == situacao_op if situacao_op else True,
                models.OrdemPagamentoOrdemBancariaEspecial.descricao_situacao_op.ilike("%{descricao_situacao_op}%") if descricao_situacao_op else True,
                models.OrdemPagamentoOrdemBancariaEspecial.data_situacao_op == date.fromisoformat(data_situacao_op) if data_situacao_op else True,
                models.OrdemPagamentoOrdemBancariaEspecial.data_emissao_ob == date.fromisoformat(data_emissao_ob) if data_emissao_ob else True,
                models.OrdemPagamentoOrdemBancariaEspecial.numero_ordem_bancaria == numero_ordem_bancaria if numero_ordem_bancaria else True,
                models.OrdemPagamentoOrdemBancariaEspecial.numero_ordem_lancamento == numero_ordem_lancamento if numero_ordem_lancamento else True,
                models.OrdemPagamentoOrdemBancariaEspecial.data_assinatura_ordenador_despesa_ob == date.fromisoformat(data_assinatura_ordenador_despesa_ob) if data_assinatura_ordenador_despesa_ob else True,
                models.OrdemPagamentoOrdemBancariaEspecial.data_assinatura_gestor_financeiro_ob == date.fromisoformat(data_assinatura_gestor_financeiro_ob) if data_assinatura_gestor_financeiro_ob else True,
                models.OrdemPagamentoOrdemBancariaEspecial.id_dh == id_dh if id_dh else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedOrdemPagamentoOrdemBancariaEspecialResponse, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
