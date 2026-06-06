```
# 🔥 yRecon - MPScanner (Massive Port Scanner)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20Android-green.svg)]()

> **Scanner de portas massivo, ultrarrápido e furtivo. Escaneie 65535 portas em segundos!**

## ✨ Funcionalidades

- 🚀 **Velocidade extrema** - 5000+ conexões simultâneas
- 🎭 **Stealth Mode** - Decoy IPs e delays aleatórios
- 🔍 **Banner Grabbing** - Identifica serviços e versões
- 🛡️ **Firewall Detection** - Detecta firewalls e WAFs
- 📊 **Múltiplos formatos** - Exporta JSON, CSV e HTML
- 🌐 **UDP Scan** - Escaneia portas UDP comuns
- ⚡ **Resolução DNS** - Aceita IPs, domínios e URLs
- 🎯 **Vulnerability Check** - Identifica portas vulneráveis

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/yRecon-MPScanner.git
cd yRecon-MPScanner

# Instale as dependências
pip install -r requirements.txt

# Execute
python3 yrecon.py
```

🚀 Uso Rápido

```bash
# Escanear um IP
python3 yrecon.py
> Opção 1
> 192.168.1.1

# Escanear um domínio
> Opção 2
> google.com

# Escanear uma URL
> Opção 3
> https://exemplo.com
```

📊 Exemplo de Saída

```
[+] PORTA 22 ABERTA - SSH
    📜 Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
[+] PORTA 80 ABERTA - HTTP
    📜 Banner: Apache/2.4.41 (Ubuntu)
[+] PORTA 443 ABERTA - HTTPS
    📜 Banner: nginx/1.18.0
```

📁 Arquivos de Saída

Arquivo Formato Descrição
scan_alvo.json JSON Dados completos em JSON
scan_alvo.csv CSV Tabela de portas abertas
scan_alvo.html HTML Relatório visual interativo

🛡️ Funcionalidades de Segurança

· Stealth Mode ativado por padrão
· Decoy IPs para evitar bloqueio
· Delay adaptativo para não sobrecarregar
· Detecção de firewall automática

📋 Requisitos

· Python 3.8+
· aiohttp
· dnspython
· asyncio

⚠️ Aviso Legal

Esta ferramenta é para fins educacionais e testes de segurança autorizados apenas. O uso não autorizado é ilegal. O autor não se responsabiliza por mau uso.

📄 Licença

MIT License - veja o arquivo LICENSE

👤 Autor

· yRecon - GitHub
