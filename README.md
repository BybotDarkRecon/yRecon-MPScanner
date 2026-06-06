
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
git clone https://github.com/BybotDarkRecon/yRecon-MPScanner.git
cd yRecon-MPScanner

# Instale as dependências
pip install -r requirements.txt

# Execute
python3 yrecon.py
```

🚀 Como Usar

```bash
python3 yrecon.py
```



```
Opção | Tipo | Exemplo
1     | IP único | 192.168.1.1
2     | Domínio  | google.com
3     | URL      | https://exemplo.com
4     | Range de IPs |192.168.1.1-192.168.1.255
5     | Lista de arquivo |targets.txt
```
---

📊 Exemplo de Saída

```
[+] PORTA 22 ABERTA - SSH
    📜 Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
    ⚠️ VULN: Weak SSH Config

[+] PORTA 80 ABERTA - HTTP
    📜 Banner: Apache/2.4.41 (Ubuntu)

[+] PORTA 443 ABERTA - HTTPS
    📜 Banner: nginx/1.18.0

============================================================
📊 RELATÓRIO FINAL
============================================================
📍 Alvo: google.com
🔍 IP: 142.250.217.46
⏱️  Tempo: 12.34s
🔌 Portas TCP abertas: 4
📡 Portas UDP abertas: 2
🛡️ Firewall: NÃO DETECTADO

✅ PORTAS TCP ABERTAS:
   🔓    22 - SSH
   🔓    80 - HTTP
   🔓   443 - HTTPS
   🔓  8080 - HTTP-PROXY
```

---

📁 Arquivos de Saída
```
Arquivo Formato Descrição
scan_alvo.json JSON Dados completos do scan em JSON
scan_alvo.csv CSV Tabela de portas abertas para Excel
scan_alvo.html HTML Relatório visual interativo com gráficos
```
---

🛡️ Funcionalidades de Segurança


· 🎭 Stealth Mode - Ativado por padrão, evita detecção

· 🎲 Decoy IPs - Rotação de IPs falsos para mascarar origem

· ⏱️ Delay Adaptativo - Ajusta automaticamente para não sobrecarregar

· 🔥 Firewall Detection - Detecta firewalls e WAFs automaticamente

---

📋 Requisitos
`
· 🐍 Python 3.8 ou superior

· 📦 aiohttp - Cliente HTTP assíncrono

· 🔧 dnspython - Resolução de DNS

· ⚡ asyncio - Concorrência assíncrona
`
