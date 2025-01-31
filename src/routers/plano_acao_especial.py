from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedPlanoAcaoEspecialResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

pa_router = APIRouter(tags=["Plano de Ação Especial"])
config = Settings()


@pa_router.get("/plano_acao_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados dos Planos de Ação Especiais.",
                response_description="Lista Paginada de Planos de Ação Especiais",
                response_model=PaginatedPlanoAcaoEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_plano_acao_especial(
    id_plano_acao: Optional[int] = Query(None, description="Identificador Único do Plano de Ação (PA)"),
    codigo_plano_acao: Optional[str] = Query(None, description="Código do Programa concatenado com o ID do Plano de Ação"),
    ano_plano_acao: Optional[int] = Query(None, description="Ano de Criação do Plano de Ação"),
    modalidade_plano_acao: Optional[str] = Query(None, description="Modalidade de Transferência do Plano de Ação"),
    situacao_plano_acao: Optional[str] = Query(None, description="Situação do Plano de Ação"),
    cnpj_beneficiario_plano_acao: Optional[str] = Query(None, description="CNPJ – Cadastro Nacional de Pessoa Jurídica do Beneficiário do Plano de Ação"),
    nome_beneficiario_plano_acao: Optional[str] = Query(None, description="Nome do Beneficiário do Plano de Ação"),
    uf_beneficiario_plano_acao: Optional[str] = Query(None, description="Sigla da Unidade de Federação"),
    codigo_banco_plano_acao: Optional[str] = Query(None, description="Código do Banco do PA"),
    codigo_situacao_dado_bancario_plano_acao: Optional[int] = Query(None, description="Código da Situação da Conta Corrente do PA"),
    nome_banco_plano_acao: Optional[str] = Query(None, description="Nome do Banco do PA"),
    numero_agencia_plano_acao: Optional[int] = Query(None, description="Número da Agência Bancária da Conta Corrente do PA"),
    dv_agencia_plano_acao: Optional[str] = Query(None, description="Dígito Verificador da Agência Bancária da Conta Corrente do PA"),
    numero_conta_plano_acao: Optional[int] = Query(None, description="Número da Conta Corrente do PA"),
    dv_conta_plano_acao: Optional[str] = Query(None, description="Dígito Verificador da Conta Corrente do PA"),
    nome_parlamentar_emenda_plano_acao: Optional[str] = Query(None, description="Nome do Parlamentar Autor da Emenda"),
    ano_emenda_parlamentar_plano_acao: Optional[str] = Query(None, description="Ano da Emenda Parlamentar"),
    codigo_parlamentar_emenda_plano_acao: Optional[str] = Query(None, description="Código do Parlamentar Autor da Emenda"),
    sequencial_emenda_parlamentar_plano_acao: Optional[int] = Query(None, description="Sequencial da Emenda Por Parlamentar no Ano"),
    numero_emenda_parlamentar_plano_acao: Optional[str] = Query(None, description="Concatenação do Ano, Código e Sequencial do Parlamentar"),
    codigo_emenda_parlamentar_formatado_plano_acao: Optional[str] = Query(None, description="Código Formatado da Emenda Parlamentar"),
    codigo_descricao_areas_politicas_publicas_plano_acao: Optional[str] = Query(None, description="Concatenação dos Códigos e Descrições dos Tipos da \
                                                                                Áreas das Políticas Públicas com os Códigos e Descrições das Áreas das Políticas Públicas"),
    descricao_programacao_orcamentaria_plano_acao: Optional[str] = Query(None, description="Concatenação das Programações Orçamentárias constantes da \
                                                                         Lei Orçamentária do ente beneficiado na qual o recurso será apropriado"),
    motivo_impedimento_plano_acao: Optional[str] = Query(None, description="Motivo do Impedimento do Plano de Ação"),
    valor_custeio_plano_acao: Optional[float] = Query(None, description="Valor Consolidado de Custeio das Emendas Parlamentares do Plano de Ação"),
    valor_investimento_plano_acao: Optional[float] = Query(None, description="Valor Consolidado de Investimento das Emendas Parlamentares do Plano de Ação"),
    id_programa: Optional[int] = Query(None, description="Identificador Único do Programa"),
    pagina: int = Query(1, ge=1, description="Número da Página"),
    tamanho_da_pagina: int = Query(config.DEFAULT_PAGE_SIZE, le=config.MAX_PAGE_SIZE, ge=1, description="Tamanho da Página"),
    dbsession: AsyncSession = Depends(get_session)
):
    params_list = [id_plano_acao, codigo_plano_acao, ano_plano_acao, modalidade_plano_acao, situacao_plano_acao, cnpj_beneficiario_plano_acao, nome_beneficiario_plano_acao,
                   uf_beneficiario_plano_acao, codigo_banco_plano_acao, codigo_situacao_dado_bancario_plano_acao, nome_banco_plano_acao, numero_agencia_plano_acao,
                    dv_agencia_plano_acao, numero_conta_plano_acao, dv_conta_plano_acao, nome_parlamentar_emenda_plano_acao, ano_emenda_parlamentar_plano_acao, codigo_parlamentar_emenda_plano_acao,
                    sequencial_emenda_parlamentar_plano_acao, numero_emenda_parlamentar_plano_acao, codigo_emenda_parlamentar_formatado_plano_acao, codigo_descricao_areas_politicas_publicas_plano_acao,
                    descricao_programacao_orcamentaria_plano_acao, motivo_impedimento_plano_acao, valor_custeio_plano_acao, valor_investimento_plano_acao, id_programa]
    
    if not any(params_list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nenhum parâmetro de consulta foi informado.")
    
    try:
        query = select(models.PlanoAcaoEspecial).where(
            and_(
                models.PlanoAcaoEspecial.id_plano_acao == id_plano_acao if id_plano_acao else True,
                models.PlanoAcaoEspecial.codigo_plano_acao == codigo_plano_acao if codigo_plano_acao else True,
                models.PlanoAcaoEspecial.ano_plano_acao == ano_plano_acao if ano_plano_acao else True,
                models.PlanoAcaoEspecial.modalidade_plano_acao.ilike(f"%{modalidade_plano_acao}%") if modalidade_plano_acao else True,
                models.PlanoAcaoEspecial.situacao_plano_acao.ilike(f"%{situacao_plano_acao}%") if situacao_plano_acao else True,
                models.PlanoAcaoEspecial.cnpj_beneficiario_plano_acao == cnpj_beneficiario_plano_acao if cnpj_beneficiario_plano_acao else True,
                models.PlanoAcaoEspecial.nome_beneficiario_plano_acao.ilike(f"%{nome_beneficiario_plano_acao}%") if nome_beneficiario_plano_acao else True,
                models.PlanoAcaoEspecial.uf_beneficiario_plano_acao.ilike(f"%{uf_beneficiario_plano_acao}%") if uf_beneficiario_plano_acao else True,
                models.PlanoAcaoEspecial.codigo_banco_plano_acao == codigo_banco_plano_acao if codigo_banco_plano_acao else True,
                models.PlanoAcaoEspecial.codigo_situacao_dado_bancario_plano_acao == codigo_situacao_dado_bancario_plano_acao if codigo_situacao_dado_bancario_plano_acao else True,
                models.PlanoAcaoEspecial.nome_banco_plano_acao.ilike(f"%{nome_banco_plano_acao}%") if nome_banco_plano_acao else True,
                models.PlanoAcaoEspecial.numero_agencia_plano_acao == numero_agencia_plano_acao if numero_agencia_plano_acao else True,
                models.PlanoAcaoEspecial.dv_agencia_plano_acao == dv_agencia_plano_acao if dv_agencia_plano_acao else True,
                models.PlanoAcaoEspecial.numero_conta_plano_acao == numero_conta_plano_acao if numero_conta_plano_acao else True,
                models.PlanoAcaoEspecial.dv_conta_plano_acao == dv_conta_plano_acao if dv_conta_plano_acao else True,
                models.PlanoAcaoEspecial.nome_parlamentar_emenda_plano_acao.ilike(f"%{nome_parlamentar_emenda_plano_acao}%") if nome_parlamentar_emenda_plano_acao else True,
                models.PlanoAcaoEspecial.ano_emenda_parlamentar_plano_acao == ano_emenda_parlamentar_plano_acao if ano_emenda_parlamentar_plano_acao else True,
                models.PlanoAcaoEspecial.codigo_parlamentar_emenda_plano_acao == codigo_parlamentar_emenda_plano_acao if codigo_parlamentar_emenda_plano_acao else True,
                models.PlanoAcaoEspecial.sequencial_emenda_parlamentar_plano_acao == sequencial_emenda_parlamentar_plano_acao if sequencial_emenda_parlamentar_plano_acao else True,
                models.PlanoAcaoEspecial.numero_emenda_parlamentar_plano_acao == numero_emenda_parlamentar_plano_acao if numero_emenda_parlamentar_plano_acao else True,
                models.PlanoAcaoEspecial.codigo_emenda_parlamentar_formatado_plano_acao == codigo_emenda_parlamentar_formatado_plano_acao if codigo_emenda_parlamentar_formatado_plano_acao else True,
                models.PlanoAcaoEspecial.codigo_descricao_areas_politicas_publicas_plano_acao.ilike(f"%{codigo_descricao_areas_politicas_publicas_plano_acao}%") if codigo_descricao_areas_politicas_publicas_plano_acao else True,
                models.PlanoAcaoEspecial.descricao_programacao_orcamentaria_plano_acao.ilike(f"%{descricao_programacao_orcamentaria_plano_acao}%") if descricao_programacao_orcamentaria_plano_acao else True,
                models.PlanoAcaoEspecial.motivo_impedimento_plano_acao.ilike(f"%{motivo_impedimento_plano_acao}%") if motivo_impedimento_plano_acao else True,
                models.PlanoAcaoEspecial.valor_custeio_plano_acao == valor_custeio_plano_acao if valor_custeio_plano_acao else True,
                models.PlanoAcaoEspecial.valor_investimento_plano_acao == valor_investimento_plano_acao if valor_investimento_plano_acao else True,
                models.PlanoAcaoEspecial.id_programa == id_programa if id_programa else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedPlanoAcaoEspecialResponse, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__repr__())