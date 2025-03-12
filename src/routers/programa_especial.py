from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, cast, Date
from src import models
from src.utils import get_session, get_paginated_data, config
from src.schemas import PaginatedResponseTemplate, PaginatedProgramaEspecialResponse
from datetime import date
from typing import Optional
from src.cache import cache


prg_router = APIRouter(tags=["Programa Especial"])



@prg_router.get("/programa_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados de Programas Especiais.",
                response_description="Lista Paginada de Programa Especial",
                response_model=PaginatedProgramaEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_programa_especial(
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),
    ano_programa: Optional[int] = Query(None, description="Ano do Programa"),
    modalidade_programa: Optional[str] = Query(None, description="Modalidade do Programa"),
    codigo_programa: Optional[str] = Query(None, description="Código do Programa"),
    id_orgao_superior_programa: Optional[int] = Query(None, description="Código SIORG do Órgão Repassador do Programa"),
    sigla_orgao_superior_programa: Optional[str] = Query(None, description="Sigla do Órgão Repassador do Programa"),
    nome_orgao_superior_programa: Optional[str] = Query(None, description="Nome do Órgão Repassador do Programa"),
    id_orgao_programa: Optional[int] = Query(None, description="Código do Programa"),
    sigla_orgao_programa: Optional[str] = Query(None, description="Sigla do Órgão do Programa"),
    nome_orgao_programa: Optional[str] = Query(None, description="Nome do Órgão do Programa"),
    id_unidade_gestora_programa: Optional[int] = Query(None, description="Código da Unidade Gestora do Órgão do Programa"),
    documentos_origem_programa: Optional[str] = Query(None, 
                                                      description="Concatenação dos Códigos Únicos para Identificação dos Dados Financeiros Disponibilizados",
                                                      pattern=r"^\d{4}[A-Z]{2}\d{5}.*$"),
    id_unidade_orcamentaria_responsavel_programa: Optional[int] = Query(None, description="Identificador Único da Unidade Orçamentária Responsável pelo Programa"),
    data_inicio_ciencia_programa: Optional[str] = Query(None, description="Data de Início para o Registro de Ciência"),
    data_fim_ciencia_programa: Optional[str] = Query(None, description="Data Final para o Registro de Ciência"),
    valor_necessidade_financeira_programa: Optional[float] = Query(None, description="Valor da Necessidade Financeira do Programa, resultado do somatório das minutas de empenho"),
    valor_total_disponibilizado_programa: Optional[float] = Query(None, description="Valor Total Disponibilizado para o Programa"),
    valor_impedido_programa: Optional[float] = Query(None, description="Valor Impedido"),
    valor_a_disponibilizar_programa: Optional[float] = Query(None, description="Valor a ser Disponibilizado"),
    valor_documentos_habeis_gerados_programa: Optional[float] = Query(None, description="Valor dos Documentos Hábeis Gerados"),
    valor_obs_geradas_programa: Optional[float] = Query(None, description="Valor das Ordens Bancárias Geradas"),
    valor_disponibilidade_atual_programa: Optional[float] = Query(None, description="Valor do Saldo Disponível para o registro atual de disponibilização"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params_list = [id_programa, ano_programa, modalidade_programa, codigo_programa, id_orgao_superior_programa, sigla_orgao_superior_programa, nome_orgao_superior_programa, id_orgao_programa, sigla_orgao_programa, nome_orgao_programa, id_unidade_gestora_programa, documentos_origem_programa, id_unidade_orcamentaria_responsavel_programa,
                   data_inicio_ciencia_programa, data_fim_ciencia_programa, valor_necessidade_financeira_programa, valor_total_disponibilizado_programa, valor_impedido_programa, valor_a_disponibilizar_programa, valor_documentos_habeis_gerados_programa, valor_obs_geradas_programa, valor_disponibilidade_atual_programa]
    if not any(params_list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nenhum parâmetro de consulta foi informado.")

    try:
        query = select(models.ProgramaEspecial).where(
            and_(
                models.ProgramaEspecial.id_programa == id_programa if id_programa else True,
                models.ProgramaEspecial.ano_programa == ano_programa if ano_programa else True,
                models.ProgramaEspecial.modalidade_programa.ilike(f"%{modalidade_programa}%") if modalidade_programa else True,
                models.ProgramaEspecial.codigo_programa == codigo_programa if codigo_programa else True,
                models.ProgramaEspecial.id_orgao_superior_programa == id_orgao_superior_programa if id_orgao_superior_programa else True,
                models.ProgramaEspecial.sigla_orgao_superior_programa.ilike(f"%{sigla_orgao_superior_programa}%") if sigla_orgao_superior_programa else True,
                models.ProgramaEspecial.nome_orgao_superior_programa.ilike(f"%{nome_orgao_superior_programa}%") if nome_orgao_superior_programa else True,
                models.ProgramaEspecial.id_orgao_programa == id_orgao_programa if id_orgao_programa else True,
                models.ProgramaEspecial.sigla_orgao_programa.ilike(f"%{sigla_orgao_programa}%") if sigla_orgao_programa else True,
                models.ProgramaEspecial.nome_orgao_programa.ilike(f"%{nome_orgao_programa}%") if nome_orgao_programa else True,
                models.ProgramaEspecial.id_unidade_gestora_programa == id_unidade_gestora_programa if id_unidade_gestora_programa else True,
                models.ProgramaEspecial.documentos_origem_programa.ilike(f"%{documentos_origem_programa}%") if documentos_origem_programa else True,
                models.ProgramaEspecial.id_unidade_orcamentaria_responsavel_programa == id_unidade_orcamentaria_responsavel_programa if id_unidade_orcamentaria_responsavel_programa else True,
                models.ProgramaEspecial.data_inicio_ciencia_programa == data_inicio_ciencia_programa if data_inicio_ciencia_programa else True,
                models.ProgramaEspecial.data_fim_ciencia_programa == data_fim_ciencia_programa if data_fim_ciencia_programa else True,
                models.ProgramaEspecial.valor_necessidade_financeira_programa == valor_necessidade_financeira_programa if valor_necessidade_financeira_programa else True,
                models.ProgramaEspecial.valor_total_disponibilizado_programa == valor_total_disponibilizado_programa if valor_total_disponibilizado_programa else True,
                models.ProgramaEspecial.valor_impedido_programa == valor_impedido_programa if valor_impedido_programa else True,
                models.ProgramaEspecial.valor_a_disponibilizar_programa == valor_a_disponibilizar_programa if valor_a_disponibilizar_programa else True,
                models.ProgramaEspecial.valor_documentos_habeis_gerados_programa == valor_documentos_habeis_gerados_programa if valor_documentos_habeis_gerados_programa else True,
                models.ProgramaEspecial.valor_obs_geradas_programa == valor_obs_geradas_programa if valor_obs_geradas_programa else True,
                models.ProgramaEspecial.valor_disponibilidade_atual_programa == valor_disponibilidade_atual_programa if valor_disponibilidade_atual_programa else True
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
