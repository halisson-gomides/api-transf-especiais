from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedDocumentoHabilEspecialResponse
from datetime import date
from typing import Optional
from appconfig import Settings

dh_router = APIRouter(tags=["Documento Hábil Especial"])
config = Settings()

@dh_router.get("/documento_habil_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Documentos hábeis Especiais.",
                response_description="Lista Paginada de Documentos hábeis Especiais",
                response_model=PaginatedDocumentoHabilEspecialResponse
                )
async def consulta_documento_habil_especial(
    id_dh: Optional[int] = Query(None, description="Identificador Único do Documento Hábil (DH)"),
    id_minuta_documento_habil: Optional[str] = Query(None, description="Padrao de Minuta de DH do tipo 2020MDH000001"),
    numero_documento_habil: Optional[str] = Query(None, description="Número do DH no formato: YYYYTTNNNNNN<br/>Ex.: 2024TF010020", examples=["2024TF010020"], max_length=12),
    situacao_dh: Optional[int] = Query(None, description="Código da Situação do DH"),
    descricao_situacao_dh: Optional[str] = Query(None, description="Descrição da Situação do DH"),
    tipo_documento_dh: Optional[str] = Query(None, description="Código do tipo do Documento Hábil"),
    ug_emitente_dh: Optional[int] = Query(None, description="Código da Unidade Gestora Emitente do Documento Hábil"),
    descricao_ug_emitente_dh: Optional[str] = Query(None, description="Nome da Unidade Gestora Emitente do Documento Hábil"),
    data_vencimento_dh: Optional[str] = Query(None, description="Data de Vencimento do Documento Hábil<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    data_emissao_dh: Optional[str] = Query(None, description="Data de Emissão do Documento Hábil<br/>Ex.: 2024-12-11", pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["2024-12-11"]),
    ug_pagadora_dh: Optional[int] = Query(None, description="Código da Unidade Gestora Pagadora do Documento Hábil"),
    descricao_ug_pagadora_dh: Optional[str] = Query(None, description="Nome da Unidade Gestora Pagadora do Documento Hábil"),
    variacao_patrimonial_diminuta_dh: Optional[str] = Query(None, description="Variação Patrimonial Diminutiva"),
    passivo_transferencia_constitucional_legal_dh: Optional[str] = Query(None, description="Passivo Transferência Legal ou Constitucional"),
    centro_custo_empenho: Optional[str] = Query(None, description="Código do Centro de Custo"),
    codigo_siorg_empenho: Optional[int] = Query(None, description="Código SIORG do Centro de Custo"),
    mes_referencia_empenho: Optional[str] = Query(None, description="Mês de Referência do Centro do Custo", min_length=2, max_length=2),
    ano_referencia_empenho: Optional[int] = Query(None, description="Ano de Referência do Centro do Custo"),
    ug_beneficiada_dh: Optional[int] = Query(None, description="Código da Unidade Gestora Beneficiada do Documento Hábil"),
    descricao_ug_beneficiada_dh: Optional[str] = Query(None, description="Nome da Unidade Gestora Beneficiada do Documento Hábil"),
    valor_dh: Optional[float] = Query(None, description="Valor do Documento Hábil.<br/>OBS: Se a Disponibilidade Financeira for menor que o valor do Empenho, mais de um Documento Hábil pode ser criado"),
    valor_rateio_dh: Optional[float] = Query(None, description="Valor do Rateio"),
    id_empenho: Optional[int] = Query(None, description="Identificador Único da Nota de Empenho (NE)"),
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
        query = select(models.DocumentoHabilEspecial).where(
            and_(
                models.DocumentoHabilEspecial.id_dh == id_dh if id_dh else True,
                models.DocumentoHabilEspecial.id_minuta_documento_habil == id_minuta_documento_habil if id_minuta_documento_habil else True,
                models.DocumentoHabilEspecial.numero_documento_habil == numero_documento_habil if numero_documento_habil else True,
                models.DocumentoHabilEspecial.situacao_dh == situacao_dh if situacao_dh else True,
                models.DocumentoHabilEspecial.descricao_situacao_dh.ilike(f"%{descricao_situacao_dh}%") if descricao_situacao_dh else True,
                models.DocumentoHabilEspecial.tipo_documento_dh.ilike(f"%{tipo_documento_dh}%") if tipo_documento_dh else True,
                models.DocumentoHabilEspecial.ug_emitente_dh == ug_emitente_dh if ug_emitente_dh else True,
                models.DocumentoHabilEspecial.descricao_ug_emitente_dh.ilike(f"%{descricao_ug_emitente_dh}%") if descricao_ug_emitente_dh else True,
                models.DocumentoHabilEspecial.data_vencimento_dh == date.fromisoformat(data_vencimento_dh) if data_vencimento_dh else True,
                models.DocumentoHabilEspecial.data_emissao_dh == date.fromisoformat(data_emissao_dh) if data_emissao_dh else True,
                models.DocumentoHabilEspecial.ug_pagadora_dh == ug_pagadora_dh if ug_pagadora_dh else True,
                models.DocumentoHabilEspecial.descricao_ug_pagadora_dh.ilike(f"%{descricao_ug_pagadora_dh}%") if descricao_ug_pagadora_dh else True,
                models.DocumentoHabilEspecial.variacao_patrimonial_diminuta_dh == variacao_patrimonial_diminuta_dh if variacao_patrimonial_diminuta_dh else True,
                models.DocumentoHabilEspecial.passivo_transferencia_constitucional_legal_dh == passivo_transferencia_constitucional_legal_dh if passivo_transferencia_constitucional_legal_dh else True,
                models.DocumentoHabilEspecial.centro_custo_empenho == centro_custo_empenho if centro_custo_empenho else True,
                models.DocumentoHabilEspecial.codigo_siorg_empenho == codigo_siorg_empenho if codigo_siorg_empenho else True,
                models.DocumentoHabilEspecial.mes_referencia_empenho == mes_referencia_empenho if mes_referencia_empenho else True,
                models.DocumentoHabilEspecial.ano_referencia_empenho == ano_referencia_empenho if ano_referencia_empenho else True,
                models.DocumentoHabilEspecial.ug_beneficiada_dh == ug_beneficiada_dh if ug_beneficiada_dh else True,
                models.DocumentoHabilEspecial.descricao_ug_beneficiada_dh.ilike(f"%{descricao_ug_beneficiada_dh}%") if descricao_ug_beneficiada_dh else True,
                models.DocumentoHabilEspecial.valor_dh == valor_dh if valor_dh else True,
                models.DocumentoHabilEspecial.valor_rateio_dh == valor_rateio_dh if valor_rateio_dh else True,
                models.DocumentoHabilEspecial.id_empenho == id_empenho if id_empenho else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedDocumentoHabilEspecialResponse, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())