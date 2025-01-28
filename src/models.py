from sqlmodel import Field, SQLModel, Relationship
import datetime as dt
from typing import List, Optional

db_schema = 'api_transferegov_transferenciasespeciais'

class BaseModel(SQLModel, table=False):
    """Base class for all SQLModel subclasses"""

    # This sets the database schema in which to create tables for all subclasses of BaseModel
    __table_args__ = {"schema": db_schema}


class ProgramaEspecial(BaseModel, table=True):    
    __tablename__ = "programa_especial"

    id_programa: int = Field(primary_key=True)
    ano_programa: int
    modalidade_programa: str
    codigo_programa: str
    id_orgao_superior_programa: int
    sigla_orgao_superior_programa: str
    nome_orgao_superior_programa: str
    id_orgao_programa: int
    sigla_orgao_programa: str
    nome_orgao_programa: str
    id_unidade_gestora_programa: int
    documentos_origem_programa: str
    id_unidade_orcamentaria_responsavel_programa: int
    data_inicio_ciencia_programa: dt.date
    data_fim_ciencia_programa: dt.date
    valor_necessidade_financeira_programa: float
    valor_total_disponibilizado_programa: float
    valor_impedido_programa: float
    valor_a_disponibilizar_programa: float
    valor_documentos_habeis_gerados_programa: float
    valor_obs_geradas_programa: float
    valor_disponibilidade_atual_programa: float


class PlanoAcaoEspecial(BaseModel, table=True):
    __tablename__ = "plano_acao_especial"

    id_plano_acao: int = Field(primary_key=True)
    codigo_plano_acao: str
    ano_plano_acao: int
    modalidade_plano_acao: str
    situacao_plano_acao: str
    cnpj_beneficiario_plano_acao: str
    nome_beneficiario_plano_acao: str
    uf_beneficiario_plano_acao: str
    codigo_banco_plano_acao: str
    codigo_situacao_dado_bancario_plano_acao: int
    nome_banco_plano_acao: str
    numero_agencia_plano_acao: int
    dv_agencia_plano_acao: str
    numero_conta_plano_acao: str
    dv_conta_plano_acao: str
    nome_parlamentar_emenda_plano_acao: str
    ano_emenda_parlamentar_plano_acao: str
    codigo_parlamentar_emenda_plano_acao: str
    sequencial_emenda_parlamentar_plano_acao: int
    numero_emenda_parlamentar_plano_acao: str
    codigo_emenda_parlamentar_formatado_plano_acao: str
    codigo_descricao_areas_politicas_publicas_plano_acao: str
    descricao_programacao_orcamentaria_plano_acao: str
    motivo_impedimento_plano_acao: str
    valor_custeio_plano_acao: float
    valor_investimento_plano_acao: float
    id_programa: int = Field(foreign_key=f"{db_schema}.programa_especial.id_programa")


class EmpenhoEspecial(BaseModel, table=True):
    __tablename__ = "empenho_especial"

    id_empenho: int = Field(primary_key=True)
    id_minuta_empenho: str
    numero_empenho: str
    situacao_empenho: int
    descricao_situacao_empenho: str
    tipo_documento_empenho: int
    descricao_tipo_documento_empenho: str
    status_processamento_empenho: str
    ug_responsavel_empenho: int
    ug_emitente_empenho: int
    descricao_ug_emitente_empenho: str
    fonte_recurso_empenho: str
    plano_interno_empenho: str
    ptres_empenho: int
    grupo_natureza_despesa_empenho: str
    natureza_despesa_empenho: str
    subitem_empenho: str
    categoria_despesa_empenho: str
    modalidade_despesa_empenho: int
    cnpj_beneficiario_empenho: str
    nome_beneficiario_empenho: str
    uf_beneficiario_empenho: str
    numero_ro_empenho: str
    data_emissao_empenho: dt.date
    prioridade_desbloqueio_empenho: int
    valor_empenho: float
    id_plano_acao: int = Field(foreign_key=f"{db_schema}.plano_acao_especial.id_plano_acao")


class DocumentoHabilEspecial(BaseModel, table=True):
    __tablename__ = "documento_habil_especial"

    id_dh: int = Field(primary_key=True)
    id_minuta_documento_habil: str
    numero_documento_habil: str
    situacao_dh: int
    descricao_situacao_dh: str
    tipo_documento_dh: str
    ug_emitente_dh: int
    descricao_ug_emitente_dh: str
    data_vencimento_dh: dt.date
    data_emissao_dh: dt.date
    ug_pagadora_dh: int
    descricao_ug_pagadora_dh: str
    variacao_patrimonial_diminuta_dh: str
    passivo_transferencia_constitucional_legal_dh: str
    centro_custo_empenho: str
    codigo_siorg_empenho: int
    mes_referencia_empenho: str
    ano_referencia_empenho: int
    ug_beneficiada_dh: int
    descricao_ug_beneficiada_dh: str
    valor_dh: float
    valor_rateio_dh: float
    id_empenho: int = Field(foreign_key=f"{db_schema}.empenho_especial.id_empenho") 


class OrdemPagamentoOrdemBancariaEspecial(BaseModel, table=True):
    __tablename__ = "ordem_pagamento_ordem_bancaria_especial"

    id_op_ob: int = Field(primary_key=True)
    data_emissao_op: dt.date
    numero_ordem_pagamento: str
    vinculacao_op: int
    situacao_op: int
    descricao_situacao_op: str
    data_situacao_op: dt.date
    data_emissao_ob: dt.date
    numero_ordem_bancaria: str
    numero_ordem_lancamento: str
    data_assinatura_ordenador_despesa_ob: dt.date
    data_assinatura_gestor_financeiro_ob: dt.date
    id_dh: int = Field(foreign_key=f"{db_schema}.documento_habil_especial.id_dh")


class HistoricoPagamentoEspecial(BaseModel, table=True):
    __tablename__ = "historico_pagamento_especial"

    id_historico_op_ob: int = Field(primary_key=True)
    data_hora_historico_op: dt.datetime
    historico_situacao_op: int
    descricao_historico_situacao_op: str
    id_op_ob: int = Field(foreign_key=f"{db_schema}.ordem_pagamento_ordem_bancaria_especial.id_op_ob")