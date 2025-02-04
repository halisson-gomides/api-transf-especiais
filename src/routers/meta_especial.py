from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from src import models
from src.utils import get_session, get_paginated_data
from src.schemas import PaginatedMetaEspecialResponse
from typing import Optional
from appconfig import Settings
from src.cache import cache

me_router = APIRouter(tags=["Meta Especial"])
config = Settings()


@me_router.get("/meta_especial",
                status_code=status.HTTP_200_OK,
                description="Retorna uma Lista Paginada dos dados das Metas Especiais.",
                response_description="Lista Paginada de Meta Especial",
                response_model=PaginatedMetaEspecialResponse
                )
@cache(ttl=config.CACHE_TTL)
async def consulta_meta_especial(
    id_executor: Optional[int] = Query(None, description="Identificador Único do Executor Especial"),
    id_meta: int = Query(None, description="Identificador Único da Meta Especial"),
    sequencial_meta: Optional[int] = Query(None, description="Sequencial da Meta Especial"),
    nome_meta: Optional[str] = Query(None, description="Nome da Meta Especial"),
    desc_meta: Optional[str] = Query(None, description="Descrição da Meta Especial"),
    un_medida_meta: Optional[str] = Query(None, description="Unidade de medida da Meta Especial"),
    qt_uniade_meta: Optional[float] = Query(None, description="Quantidade da Meta Especial", ge=0),
    vl_custeio_emenda_especial_meta: Optional[float] = Query(None, description="Valor de custeio oriundo de emenda para Meta Especial"),
    vl_investimento_emenda_especial_meta: Optional[float] = Query(None, description="Valor de investimento oriundo de emenda para Meta Especial"),
    vl_custeio_recursos_proprios_meta: Optional[float] = Query(None, description="Valor de custeio oriundo de recursos próprios para Meta Especial"),
    vl_investimento_recursos_proprios_meta: Optional[float] = Query(None, description="Valor de investimento oriundo de recursos próprios para Meta Especial"),
    vl_custeio_rendimento_meta: Optional[float] = Query(None, description="Valor de custeio oriundo de rendimentos para Meta Especial"),
    vl_investimento_rendimento_meta: Optional[float] = Query(None, description="Valor de investimento oriundo de rendimentos para Meta Especial"),
    vl_custeio_doacao_meta: Optional[float] = Query(None, description="Valor de custeio oriundo de doação para Meta Especial"),
    vl_investimento_doacao_meta: Optional[float] = Query(None, description="Valor de investimento oriundo de doação para Meta Especial"),
    qt_meses_meta: Optional[int] = Query(None, description="Prazo de execução do Plano de Trabalho (em meses)"),
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
        query = select(models.MetaEspecial).where(
            and_(
                models.MetaEspecial.id_executor == id_executor if id_executor else True,
                models.MetaEspecial.id_meta == id_meta if id_meta else True,
                models.MetaEspecial.sequencial_meta == sequencial_meta if sequencial_meta else True,
                models.MetaEspecial.nome_meta.ilike(f"%{nome_meta}%") if nome_meta else True,
                models.MetaEspecial.desc_meta.ilike(f"%{desc_meta}%") if desc_meta else True,
                models.MetaEspecial.un_medida_meta.ilike(f"%{un_medida_meta}%") if un_medida_meta else True,
                models.MetaEspecial.qt_uniade_meta == qt_uniade_meta if qt_uniade_meta else True,
                models.MetaEspecial.vl_custeio_emenda_especial_meta == vl_custeio_emenda_especial_meta if vl_custeio_emenda_especial_meta else True,
                models.MetaEspecial.vl_investimento_emenda_especial_meta == vl_investimento_emenda_especial_meta if vl_investimento_emenda_especial_meta else True,
                models.MetaEspecial.vl_custeio_recursos_proprios_meta == vl_custeio_recursos_proprios_meta if vl_custeio_recursos_proprios_meta else True,
                models.MetaEspecial.vl_investimento_recursos_proprios_meta == vl_investimento_recursos_proprios_meta if vl_investimento_recursos_proprios_meta else True,
                models.MetaEspecial.vl_custeio_rendimento_meta == vl_custeio_rendimento_meta if vl_custeio_rendimento_meta else True,
                models.MetaEspecial.vl_investimento_rendimento_meta == vl_investimento_rendimento_meta if vl_investimento_rendimento_meta else True,
                models.MetaEspecial.vl_custeio_doacao_meta == vl_custeio_doacao_meta if vl_custeio_doacao_meta else True,
                models.MetaEspecial.vl_investimento_doacao_meta == vl_investimento_doacao_meta if vl_investimento_doacao_meta else True,
                models.MetaEspecial.qt_meses_meta == qt_meses_meta if qt_meses_meta else True
            )
        )
        result = await get_paginated_data(query=query,
                                          dbsession=dbsession,
                                          response_schema=PaginatedMetaEspecialResponse, 
                                          current_page=pagina, 
                                          records_per_page=tamanho_da_pagina)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro ao consultar Plano de Trabalho: {e.__repr__()}")