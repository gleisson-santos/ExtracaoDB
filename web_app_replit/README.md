# Sistema Web de Extração de Dados SCI

Aplicação web para automação de extração de dados do SCI Web usando Selenium.

## 📋 Estrutura

```
web_app_replit/
├── app.py                 # Backend Flask + SocketIO
├── funcoes_web.py         # Funções de automação Selenium
├── requirements.txt       # Dependências
├── .env                   # Variáveis de ambiente
├── .gitignore            # Arquivos ignorados
├── templates/
│   └── index.html        # Frontend HTML/CSS/JS
└── README.md
```

## 🚀 Como rodar no Replit

### 1. Criar um novo Replit
- Vá para [replit.com](https://replit.com)
- Clique "Create Replit"
- Selecione "Python" como linguagem

### 2. Clonar ou copiar os arquivos
```bash
# Opção A: Clonar o repositório
git clone [seu_repo_url]

# Opção B: Copiar manualmente
# - Copie o conteúdo de cada arquivo
# - Cole no editor do Replit
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
- Clique no ícone de chave (Secrets) no Replit
- Adicione:
  - `SCI_USER` = seu usuário
  - `SCI_PASSWORD` = sua senha

### 5. Rodar a aplicação
```bash
python app.py
```

A aplicação será acessível em: `https://[seu-replit].replit.dev`

## 🔧 Variáveis de Ambiente

Crie um arquivo `.env` na raiz com:

```
SCI_USER=seu_usuario
SCI_PASSWORD=sua_senha
FLASK_ENV=production
DEBUG=False
```

## 📝 Uso

1. Abra a aplicação no navegador
2. Preencha as datas (formato DD/MM/YYYY)
3. Clique em "Iniciar Extração"
4. Acompanhe o progresso em tempo real
5. Baixe os dados quando concluído

## 🔄 Fluxo WebSocket

```
Cliente (Browser) <--> WebSocket <--> Servidor (Flask)
         |                                     |
         |                                Selenium
         |                                     |
         +------ Progresso em Tempo Real -----+
```

## ⚙️ Configuração dos Filtros

Edite em `main.py` (ou defina dinamicamente):

```python
filtro = [
    "form-filtroAcss-dlgFilterPrefs-tableUser-8-j_idt364",
    "form-filtroAcss-dlgFilterPrefs-tableUser-9-j_idt364"
]
```

## 🐛 Troubleshooting

### Erro: "Element not found"
- Os IDs do site podem ter mudado
- Inspecione o navegador (F12) e atualize os IDs em `funcoes_web.py`

### Erro: "TimeoutException"
- Aumente o tempo de espera em `esperar_clicavel()` ou `esperar_sumir()`
- Verifique se o site está lento

### Chrome driver não funciona
```bash
pip install --upgrade webdriver-manager
```

## 📊 Monitoramento

O log em tempo real mostra:
- Login realizado
- Filtros aplicados
- Datas processadas
- Planilhas exportadas
- Erros encontrados

## 🔒 Segurança

⚠️ **Importante:**
- Nunca deixe credenciais no código
- Use variáveis de ambiente
- Em produção, use HTTPS
- Implemente autenticação de usuário

## 📱 Responsividade

A interface foi otimizada para:
- Desktop
- Tablet
- Mobile

## 🚀 Deploy em Produção

### Render.com
```bash
# 1. Criar repositório Git
git init
git add .
git commit -m "Initial commit"

# 2. Push para GitHub
git push origin main

# 3. Conectar no Render.com
# - Autorizar GitHub
# - Selecionar repositório
# - Configurar variáveis de ambiente
# - Deploy automático
```

### Railway.app
Similar ao Render - conecte seu GitHub e configure.

## 📞 Suporte

Para problemas ou dúvidas, abra uma issue no GitHub.

## 📄 Licença

MIT License
