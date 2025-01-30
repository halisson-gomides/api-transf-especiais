from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedEmpenhoEspecialResponse
from typing import Optional
from datetime import date
from appconfig import Settings
from src.cache import cache

em_router = APIRouter(tags=["Empenho Especial"])
config = Settings()

@em_router.get("/empenho_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Empenhos Especiais.",
                response_description="Lista Paginada de Empenhos Especiais",
                response_model=PaginatedEmpenhoEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_empenho_especial(
    id_empenho: Optional[int] = Query(None, description="Identificador Único da Nota de Empenho (NE)"),
    id_minuta_empenho: Optional[str] = Query(None, description="Número da Minuta gerado para Nota de Empenho, utiliza o Número Interno e Ano de Emissão"),
    numero_empenho: Optional[str] = Query(None, description="Número da Nota de Empenho gerada e enviada pelo SIAFI (Sistema Integrado de Administração Financeira)"),
    situacao_empenho: Optional[int] = Query(None, description="Situação da Nota de Empenho (NE)"),
    descricao_situacao_empenho: Optional[str] = Query(None, description="Descrição da Situação da Nota de Empenho (NE)"),
    tipo_documento_empenho: Optional[int] = Query(None, description="Tipo da Nota de Empenho"),
    descricao_tipo_documento_empenho: Optional[str] = Query(None, description="Descrição do Tipo da Nota de Empenho"),
    status_processamento_empenho: Optional[str] = Query(None, description="Indica o status do processamento em lote da Nota de Empenho"),
    ug_responsavel_empenho: Optional[int] = Query(None, description="Código da Unidade Gestora Responsável da Nota de Empenho"),
    ug_emitente_empenho: Optional[int] = Query(None, description="Código da Unidade Gestora Emitente da Nota de Empenho"),
    descricao_ug_emitente_empenho: Optional[str] = Query(None, description="Nome da Unidade Gestora Emitente da Nota de Empenho"),
    fonte_recurso_empenho: Optional[str] = Query(None, description="Fonte de Recurso da Nota de Empenho no SIAFI (Sistema Integrado de Administração Financeira)"),
    plano_interno_empenho: Optional[str] = Query(None, description="Instrumento de planejamento e de acompanhamento da ação planejada, usado como forma de detalhamento desta, \
                                                 de uso exclusivo de cada Ministério/órgão, com as seguintes características: - Há um atributo na tabela de órgão para indicar \
                                                 se o órgão utiliza ou não o Plano Interno (PI). Este atributo é mantido pela STN decorrente da solicitação do órgão. \
                                                 - A unidade setorial de orçamento do órgão é responsável por registrar na tabela os códigos de PI. \
                                                 - O SIAFI (Sistema Integrado de Administração Financeira), de acordo com o cadastramento previsto acima, só aceitará a emissão de \
                                                 nota de empenho com o código de PI existente. - Os códigos de PI poderão ter até 11 (onze) posições alfa-numéricas"),
    ptres_empenho: Optional[int] = Query(None, description="Número do Programa de Trabalho Resumido"),
    grupo_natureza_despesa_empenho: Optional[str] = Query(None, description="Primeiro dígito do Código da Natureza de Despesa no SIAFI"),
    natureza_despesa_empenho: Optional[str] = Query(None, description="Código da Natureza de Despesa no SIAFI (Sistema Integrado de Administração Financeira)"),
    subitem_empenho: Optional[str] = Query(None, description="Código do Subitem da Natureza de Despesa no SIAFI (Sistema Integrado de Administração Financeira)"),
    categoria_despesa_empenho: Optional[str] = Query(None, description="Código da Categoria de Despesa associada à Nota de Empenho"),
    modalidade_despesa_empenho: Optional[int] = Query(None, description="Código da Modalidade de Despesa"),
    cnpj_beneficiario_empenho: Optional[str] = Query(None, description="CNPJ do Beneficiário"),
    nome_beneficiario_empenho: Optional[str] = Query(None, description="Nome do Beneficiário"),
    uf_beneficiario_empenho: Optional[str] = Query(None, description="Sigla da Unidade da Federação do Beneficiário"),
    numero_ro_empenho: Optional[str] = Query(None, description="Número da lista gerado e enviado pelo SIAFI (Sistema Integrado de Administração Financeira)"),
    data_emissao_empenho: Optional[str] = Query(None, description="Data de envio ao SIAFI (Sistema Integrado de Administração Financeira)", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    prioridade_desbloqueio_empenho: Optional[int] = Query(None, description="Indicador de prioridade no desbloqueio de recursos"),
    valor_empenho: Optional[float] = Query(None, description="Valor total da Nota de Empenho"),
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação (PA)"),
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
        query = select(models.EmpenhoEspecial).where(
            and_(
                models.EmpenhoEspecial.id_empenho == id_empenho if id_empenho else True,
                models.EmpenhoEspecial.id_minuta_empenho == id_minuta_empenho if id_minuta_empenho else True,
                models.EmpenhoEspecial.numero_empenho == numero_empenho if numero_empenho else True,
                models.EmpenhoEspecial.situacao_empenho == situacao_empenho if situacao_empenho else True,
                models.EmpenhoEspecial.descricao_situacao_empenho.ilike(f"%{descricao_situacao_empenho}%") if descricao_situacao_empenho else True,
                models.EmpenhoEspecial.tipo_documento_empenho == tipo_documento_empenho if tipo_documento_empenho else True,
                models.EmpenhoEspecial.descricao_tipo_documento_empenho.ilike(f"%{descricao_tipo_documento_empenho}%") if descricao_tipo_documento_empenho else True,
                models.EmpenhoEspecial.status_processamento_empenho.ilike(f"%{status_processamento_empenho}%") if status_processamento_empenho else True,
                models.EmpenhoEspecial.ug_responsavel_empenho == ug_responsavel_empenho if ug_responsavel_empenho else True,
                models.EmpenhoEspecial.ug_emitente_empenho == ug_emitente_empenho if ug_emitente_empenho else True,
                models.EmpenhoEspecial.descricao_ug_emitente_empenho.ilike(f"%{descricao_ug_emitente_empenho}%") if descricao_ug_emitente_empenho else True,
                models.EmpenhoEspecial.fonte_recurso_empenho == fonte_recurso_empenho if fonte_recurso_empenho else True,
                models.EmpenhoEspecial.plano_interno_empenho.ilike(f"%{plano_interno_empenho}%") if plano_interno_empenho else True,
                models.EmpenhoEspecial.ptres_empenho == ptres_empenho if ptres_empenho else True,
                models.EmpenhoEspecial.grupo_natureza_despesa_empenho == grupo_natureza_despesa_empenho if grupo_natureza_despesa_empenho else True,
                models.EmpenhoEspecial.natureza_despesa_empenho == natureza_despesa_empenho if natureza_despesa_empenho else True,
                models.EmpenhoEspecial.subitem_empenho == subitem_empenho if subitem_empenho else True,
                models.EmpenhoEspecial.categoria_despesa_empenho.ilike(f"%{categoria_despesa_empenho}%") if categoria_despesa_empenho else True,
                models.EmpenhoEspecial.modalidade_despesa_empenho == modalidade_despesa_empenho if modalidade_despesa_empenho else True,
                models.EmpenhoEspecial.cnpj_beneficiario_empenho.ilike(f"%{cnpj_beneficiario_empenho}%") if cnpj_beneficiario_empenho else True,
                models.EmpenhoEspecial.nome_beneficiario_empenho.ilike(f"%{nome_beneficiario_empenho}%") if nome_beneficiario_empenho else True,
                models.EmpenhoEspecial.uf_beneficiario_empenho.ilike(f"%{uf_beneficiario_empenho}%") if uf_beneficiario_empenho else True,
                models.EmpenhoEspecial.numero_ro_empenho == numero_ro_empenho if numero_ro_empenho else True,
                models.EmpenhoEspecial.data_emissao_empenho == date.fromisoformat(data_emissao_empenho) if data_emissao_empenho else True,
                models.EmpenhoEspecial.prioridade_desbloqueio_empenho == prioridade_desbloqueio_empenho if prioridade_desbloqueio_empenho else True,
                models.EmpenhoEspecial.valor_empenho == valor_empenho if valor_empenho else True,
                models.EmpenhoEspecial.id_plano_acao == id_plano_acao if id_plano_acao else True                
            )
        )

        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedEmpenhoEspecialResponse, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())
    
