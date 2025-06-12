
# Estrutura do Projeto: `django_scaffolder`

```text
scripts/
└── django_scaffolder/
```

## Arquivos e Diretórios

### `README.md`
Documento principal de apresentação da CLI `django_scaffolder`, instruções de uso, instalação e visão geral.

---

### `cli/`
- **`main.py`**: Ponto de entrada da CLI, onde os comandos são recebidos, processados e encaminhados aos geradores e utilitários.

---

### `docs/`
- **`architecture.md`**: Documento que descreve a arquitetura interna da CLI e sua organização em módulos, templates e utilitários.

---

### `example_project/`
Projeto Django de exemplo gerado para testes e demonstração.

- **`Dockerfile`, `docker-compose.yaml`**: Configuração do ambiente com Docker.
- **`README.md`**: Instruções de uso do projeto exemplo.
- **`docs/info.txt`**: Informações gerais.
- **`envs/`**: Variáveis de ambiente e configurações.
- **`http/v1_default.http`**: Requisições HTTP para teste (Insomnia, HTTPie etc.).
- **`pyproject.toml`, `pytest.ini`, `requirements.txt`**: Dependências e configs de build/teste.

#### `src/`
Código-fonte principal do projeto Django.

##### `core/`
Infraestrutura compartilhada do projeto (middlewares, autenticação, etc.).

##### `django_app/`
Aplicação Django principal.

- `__shared/`: Recursos compartilhados:
  - `config.py`: Configurações globais
  - `containers.py`: Injeção de dependência
  - `routes.py`: Roteamento
- `asgi.py`, `wsgi.py`, `settings.py`, `urls.py`: Configurações padrão Django

##### `modules/v1/default/`
Estrutura de um módulo completo:

- `admin.py`: Registro no Django Admin
- `api.py`: Endpoints customizados
- `apps.py`: Configuração da app
- `container.py`: Configuração do módulo
- `management/commands/seed_default.py`: Comando de seed
- `migrations/`: Migrações do Django
- `models.py`: Model principal
- `repositories.py`: Camada de acesso a dados
- `serializers.py`: Serialização de dados
- `services.py`: Regras de negócio
- `tests/`, `tests.py`: Testes da aplicação
- `urls.py`: Rotas
- `views.py`: Controladores

##### `templates/`
Templates HTML para renderização frontend (admin, auth, layouts e páginas).

---

### `generators/`

#### `infra/`
Geradores de infraestrutura:

- `actions_generator.py`: Gera actions
- `database_generator.py`: Configuração do banco
- `history_generator.py`: Histórico/Changelog
- `http_generator.py`: Geração da interface HTTP
- `modules_generator.py`: Criação de novos módulos

#### `module/`
Geradores de componentes de módulos:

- `admin_generator.py`: Gera admin.py
- `api_generator.py`: Gera api.py
- `apps_generator.py`: Gera apps.py
- `base.py`: Classe base para os geradores
- `container_generator.py`: Gera container.py
- `filters_generator.py`: Filtros/queries
- `models_generator.py`: Criação de model
- `repositories_generator.py`: Camada de dados
- `routes_generator.py`: Gera rotas
- `seeds_generator.py`: Gera comandos de seed
- `serializers_generator.py`: Serialização
- `services_generator.py`: Lógica de negócios
- `tests_generator.py`: Estrutura de testes
- `urls_generator.py`: Rotas do Django
- `views_generator.py`: Views/controladores

---

### `templates/`
Templates Python usados pelos geradores para criar os arquivos:

- `*_template.py`: Cada um é um modelo de geração de arquivo (ex: models, views, urls, etc.)
- `base.py`: Base comum para os templates

---

### `utilities/`
Utilitários de apoio à CLI:

- `base.py`: Integra todos os utilitários
- `commands.py`: Funções utilizadas na CLI
- `constants.py`: Variáveis fixas (pastas, nomes, etc.)
- `display.py`: Exibição estilizada no console
- `fields.py`: Manipulação de campos do model
- `inspections.py`: Inspeções no projeto (models, actions, arquivos)
- `parser.py`: Manipulação de nomes e estruturas
- `requirements.py`: Verificação de dependências
- `tree.py`: Exibição da árvore do projeto
