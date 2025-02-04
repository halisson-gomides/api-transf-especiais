from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
from typing import List, Optional
import datetime as dt

class ProgramaEspecialResponse(BaseModel):  
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid") 

    id_programa: Optional[int]
    ano_programa: Optional[int]
    modalidade_programa: Optional[str]
    codigo_programa: Optional[str]
    id_orgao_superior_programa: Optional[int]
    sigla_orgao_superior_programa: Optional[str]
    nome_orgao_superior_programa: Optional[str]
    id_orgao_programa: Optional[int]
    sigla_orgao_programa: Optional[str]
    nome_orgao_programa: Optional[str]
    id_unidade_gestora_programa: Optional[int]
    documentos_origem_programa: Optional[str]
    id_unidade_orcamentaria_responsavel_programa: Optional[int]
    data_inicio_ciencia_programa: Optional[dt.date]
    data_fim_ciencia_programa: Optional[dt.date]
    valor_necessidade_financeira_programa: Optional[float]
    valor_total_disponibilizado_programa: Optional[float]
    valor_impedido_programa: Optional[float]
    valor_a_disponibilizar_programa: Optional[float]
    valor_documentos_habeis_gerados_programa: Optional[float]
    valor_obs_geradas_programa: Optional[float]
    valor_disponibilidade_atual_programa: Optional[float]


class PaginatedProgramaEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[ProgramaEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class PlanoAcaoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid") 

    id_plano_acao: int
    codigo_plano_acao: Optional[str]
    ano_plano_acao: Optional[int]
    modalidade_plano_acao: Optional[str]
    situacao_plano_acao: Optional[str]
    cnpj_beneficiario_plano_acao: Optional[str]
    nome_beneficiario_plano_acao: Optional[str]
    uf_beneficiario_plano_acao: Optional[str]
    codigo_banco_plano_acao: Optional[str]
    codigo_situacao_dado_bancario_plano_acao: Optional[int]
    nome_banco_plano_acao: Optional[str]
    numero_agencia_plano_acao: Optional[int]
    dv_agencia_plano_acao: Optional[str]
    numero_conta_plano_acao: Optional[int]
    dv_conta_plano_acao: Optional[str]
    nome_parlamentar_emenda_plano_acao: Optional[str]
    ano_emenda_parlamentar_plano_acao: Optional[str]
    codigo_parlamentar_emenda_plano_acao: Optional[str]
    sequencial_emenda_parlamentar_plano_acao: Optional[int]
    numero_emenda_parlamentar_plano_acao: Optional[str]
    codigo_emenda_parlamentar_formatado_plano_acao: Optional[str]
    codigo_descricao_areas_politicas_publicas_plano_acao: Optional[str]
    descricao_programacao_orcamentaria_plano_acao: Optional[str]
    motivo_impedimento_plano_acao: Optional[str]
    valor_custeio_plano_acao: Optional[float]
    valor_investimento_plano_acao: Optional[float]
    id_programa: Optional[int]


class PaginatedPlanoAcaoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[PlanoAcaoEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class EmpenhoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_empenho: int
    id_minuta_empenho: Optional[str]
    numero_empenho: Optional[str]
    situacao_empenho: Optional[int]
    descricao_situacao_empenho: Optional[str]
    tipo_documento_empenho: Optional[int]
    descricao_tipo_documento_empenho: Optional[str]
    status_processamento_empenho: Optional[str]
    ug_responsavel_empenho: Optional[int]
    ug_emitente_empenho: Optional[int]
    descricao_ug_emitente_empenho: Optional[str]
    fonte_recurso_empenho: Optional[str]
    plano_interno_empenho: Optional[str]
    ptres_empenho: Optional[int]
    grupo_natureza_despesa_empenho: Optional[str]
    natureza_despesa_empenho: Optional[str]
    subitem_empenho: Optional[str]
    categoria_despesa_empenho: Optional[str]
    modalidade_despesa_empenho: Optional[int]
    cnpj_beneficiario_empenho: Optional[str]
    nome_beneficiario_empenho: Optional[str]
    uf_beneficiario_empenho: Optional[str]
    numero_ro_empenho: Optional[str]
    data_emissao_empenho: Optional[dt.date]
    prioridade_desbloqueio_empenho: Optional[int]
    valor_empenho: Optional[float]
    id_plano_acao: Optional[int]


class PaginatedEmpenhoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[EmpenhoEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class DocumentoHabilEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid") 

    id_dh: int
    id_minuta_documento_habil: Optional[str]
    numero_documento_habil: Optional[str]
    situacao_dh: Optional[int]
    descricao_situacao_dh: Optional[str]
    tipo_documento_dh: Optional[str]
    ug_emitente_dh: Optional[int]
    descricao_ug_emitente_dh: Optional[str]
    data_vencimento_dh: Optional[dt.date]
    data_emissao_dh: Optional[dt.date]
    ug_pagadora_dh: Optional[int]
    descricao_ug_pagadora_dh: Optional[str]
    variacao_patrimonial_diminuta_dh: Optional[str]
    passivo_transferencia_constitucional_legal_dh: Optional[str]
    centro_custo_empenho: Optional[str]
    codigo_siorg_empenho: Optional[int]
    mes_referencia_empenho: Optional[str]
    ano_referencia_empenho: Optional[int]
    ug_beneficiada_dh: Optional[int]
    descricao_ug_beneficiada_dh: Optional[str]
    valor_dh: Optional[float]
    valor_rateio_dh: Optional[float]
    id_empenho: Optional[int]


class PaginatedDocumentoHabilEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[DocumentoHabilEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class OrdemPagamentoOrdemBancariaEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid") 

    id_op_ob : int
    data_emissao_op : Optional[dt.date]
    numero_ordem_pagamento : Optional[str]
    vinculacao_op : Optional[int]
    situacao_op : Optional[int]
    descricao_situacao_op : Optional[str]
    data_situacao_op : Optional[dt.date]
    data_emissao_ob : Optional[dt.date]
    numero_ordem_bancaria : Optional[str]
    numero_ordem_lancamento : Optional[str]
    data_assinatura_ordenador_despesa_ob : Optional[dt.date]
    data_assinatura_gestor_financeiro_ob : Optional[dt.date]
    id_dh : Optional[int]


class PaginatedOrdemPagamentoOrdemBancariaEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[OrdemPagamentoOrdemBancariaEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class HistoricoPagamentoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid") 

    id_historico_op_ob: int
    data_hora_historico_op: Optional[dt.datetime]
    historico_situacao_op: Optional[int]
    descricao_historico_situacao_op: Optional[str]
    id_op_ob: Optional[int]


class PaginatedHistoricoPagamentoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[HistoricoPagamentoEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class RelatorioGestaoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid") 

    id_relatorio_gestao: int
    situacao_relatorio_gestao: Optional[str]    
    parecer_relatorio_gestao: Optional[str]
    id_plano_acao: Optional[int]


class PaginatedRelatorioGestaoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[RelatorioGestaoEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class PlanoTrabalhoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid") 

    id_plano_trabalho: int
    situacao_plano_trabalho: Optional[str]
    ind_orcamento_proprio_plano_trabalho: Optional[str]
    data_inicio_execucao_plano_trabalho: Optional[dt.datetime]
    data_fim_execucao_plano_trabalho: Optional[dt.datetime]
    prazo_execucao_meses_plano_trabalho: Optional[int]
    id_plano_acao: Optional[int]
    classificacao_orcamentaria_pt: Optional[str]
    ind_justificativa_prorrogacao_atraso_pt: Optional[bool]
    ind_justificativa_prorrogacao_paralizacao_pt: Optional[bool]
    justificativa_prorrogacao_pt: Optional[str]


class PaginatedPlanoTrabalhoEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[PlanoTrabalhoEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class ExecutorEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_plano_acao: Optional[int]
    id_executor: int
    cnpj_executor: Optional[str]
    nome_executor: Optional[str]
    objeto_executor: Optional[str]
    vl_custeio_executor: Optional[float]
    vl_investimento_executor: Optional[float]


class PaginatedExecutorEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[ExecutorEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class MetaEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_executor: Optional[int]
    id_meta: int
    sequencial_meta: Optional[int]
    nome_meta: Optional[str]
    desc_meta: Optional[str]
    un_medida_meta: Optional[str]
    qt_uniade_meta: Optional[float]
    vl_custeio_emenda_especial_meta: Optional[float]
    vl_investimento_emenda_especial_meta: Optional[float]
    vl_custeio_recursos_proprios_meta: Optional[float]
    vl_investimento_recursos_proprios_meta: Optional[float]
    vl_custeio_rendimento_meta: Optional[float]
    vl_investimento_rendimento_meta: Optional[float]
    vl_custeio_doacao_meta: Optional[float]
    vl_investimento_doacao_meta: Optional[float]
    qt_meses_meta: Optional[int]


class PaginatedMetaEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[MetaEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int


class FinalidadeEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True, extra="forbid")

    id_executor: int
    cd_area_politica_publica_tipo_pt: Optional[int]
    area_politica_publica_tipo_pt: Optional[str]
    cd_area_politica_publica_pt: Optional[int]
    area_politica_publica_pt: Optional[str]


class PaginatedFinalidadeEspecialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    data: List[FinalidadeEspecialResponse]
    total_pages: int
    total_items: int
    page_number: int
    page_size: int