
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    DATABASE_URL: str
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
    ]
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100