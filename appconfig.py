
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
    CACHE_SERVER_URL: str        
    CACHE_TTL: str = "30m"    
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_TAGS: list = [
        {
            "name": "Programa Especial",
            "description": "Dados relativos às emendas de programa especial.",
        },
        {
            "name": "Plano de Ação Especial",
            "description": "Dados relativos aos planos de ação especiais.",            
        },
        {
            "name": "Empenho Especial",
            "description": "Dados relativos a empenhos especiais.",            
        },
        {
            "name": "Documento Hábil Especial",
            "description": "Dados relativos a documentos hábeis especiais.",            
        },
        {
            "name": "Ordem de pagamento e Ordem bancária Especial",
            "description": "Dados relativos a ordens de pagamento e bancária especiais.",            
        },
        {
            "name": "Histórico de Pagamento Especial",
            "description": "Dados relativos aos históricos de pagamento especiais.",            
        },
        {
            "name": "Relatório de Gestão Especial",
            "description": "Dados relativos a relatório de gestão especiais.",            
        },
        {
            "name": "Plano de Trabalho Especial",
            "description": "Dados relativos a planos de trabalho especiais.",            
        },
        {
            "name": "Executor Especial",
            "description": "Dados relativos a executores especiais.",            
        },
        {
            "name": "Meta Especial",
            "description": "Dados relativos a metas especiais.",            
        },
        {
            "name": "Finalidade Especial",
            "description": "Dados relativos a finalidades especiais.",            
        },
    ]
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 200
    ERROR_MESSAGE_NO_PARAMS: str = "Nenhum parâmetro de consulta foi informado."
    ERROR_MESSAGE_INTERNAL: str = "Erro Interno Inesperado."
    STATS_USER: str 
    STATS_PASSWORD: str