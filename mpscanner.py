#!/usr/bin/env python3
# yRecon - MPScanner V1.0
# "Massive Port Scanner"

import asyncio
import socket
import time
import sys
import json
import csv
import random
import ssl
import aiohttp
import dns.resolver
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import ipaddress
import os

# Cores
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
B = '\033[94m'
M = '\033[95m'
W = '\033[0m'

def print_banner():
    banner = f"""
{R}       ______                                                
{R}      (_____ \                                               
{R} _   _ _____) )_____  ____ ___  ____     _____               
{R}| | | |  __  /| ___ |/ ___) _ \|  _ \   (_____)              
{R}| |_| | |  \ \| ____( (__| |_| | | | |                       
{R} \__  |_|   |_|_____)\____)___/|_| |_|                       
{R}(____/                                                       
{R} _______ ______   ______                                     
{R}(_______|_____ \ / _____)                                    
{R} _  _  _ _____) | (____   ____ _____ ____  ____  _____  ____ 
{R}| ||_|| |  ____/ \____ \ / ___|____ |  _ \|  _ \| ___ |/ ___)
{R}| |   | | |      _____) | (___/ ___ | | | | | | | ____| |    
{R}|_|   |_|_|     (______/ \____)_____|_| |_|_| |_|_____)_|    
{R}                                                             
{R}╔═══════════════════════════════════════════════════════════════╗
{R}║               {C}yRecon - MPScanner V1.0{R}                         ║
{R}║                {Y}Massive Port Scanner{R}                           ║
{R}║{M}Stealth | Firewall Detection | Banner Grabbing | HTML/CSV{R}      ║
{R}╚═══════════════════════════════════════════════════════════════╝{W}
"""
    print(banner)

class MPScannerV1:
    def __init__(self, target):
        self.original_target = target
        self.target_ip = None
        self.target_host = None
        self.open_ports = []
        self.service_versions = {}
        self.firewall_detected = False
        self.start_time = None
        self.end_time = None
        self.total_ports = 65535
        self.scan_progress = 0
        self.udp_open_ports = []
        
        # Configurações máximas sem travar
        self.max_concurrent = 5000
        self.scan_timeout = 0.2
        self.stealth_mode = True
        self.decoy_ips = ['8.8.8.8', '1.1.1.1', '4.2.2.4', '208.67.222.222']
        
        self.resolve_target(target)
        
        self.services = {
            20: 'FTP-DATA', 21: 'FTP', 22: 'SSH', 23: 'TELNET', 25: 'SMTP',
            53: 'DNS', 67: 'DHCP', 68: 'DHCP', 69: 'TFTP', 80: 'HTTP',
            110: 'POP3', 111: 'RPC', 123: 'NTP', 135: 'RPC', 137: 'NETBIOS',
            138: 'NETBIOS', 139: 'NETBIOS', 143: 'IMAP', 161: 'SNMP', 162: 'SNMP',
            389: 'LDAP', 443: 'HTTPS', 445: 'SMB', 465: 'SMTPS', 514: 'SYSLOG',
            587: 'SMTP', 636: 'LDAPS', 993: 'IMAPS', 995: 'POP3S',
            1433: 'MSSQL', 1521: 'ORACLE', 1723: 'PPTP', 3306: 'MYSQL',
            3389: 'RDP', 5432: 'POSTGRES', 5900: 'VNC', 5901: 'VNC',
            6379: 'REDIS', 8080: 'HTTP-PROXY', 8443: 'HTTPS-ALT', 27017: 'MONGODB'
        }
        
        self.udp_services = {
            53: 'DNS', 67: 'DHCP', 68: 'DHCP', 69: 'TFTP', 123: 'NTP',
            161: 'SNMP', 162: 'SNMP', 514: 'SYSLOG', 520: 'RIP'
        }
        
        self.vulnerable_ports = {
            21: 'FTP Anonymous Login', 22: 'Weak SSH Config',
            23: 'Telnet Insecure', 3306: 'MySQL Default Creds',
            3389: 'RDP Vulnerable', 5900: 'VNC No Auth',
            6379: 'Redis No Auth', 27017: 'MongoDB No Auth'
        }
    
    def resolve_target(self, target):
        target = target.strip()
        if target.startswith('http://') or target.startswith('https://'):
            target = target.split('//')[1].split('/')[0].split(':')[0]
        
        self.target_host = target
        
        try:
            ipaddress.ip_address(target)
            self.target_ip = target
            print(f"{G}[+] Alvo IP: {self.target_ip}{W}")
        except:
            try:
                self.target_ip = socket.gethostbyname(target)
                print(f"{G}[+] {target} -> {self.target_ip}{W}")
            except:
                print(f"{R}[!] Não resolveu: {target}{W}")
                self.target_ip = None
    
    async def grab_banner(self, port, timeout=1):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.target_ip, port),
                timeout=timeout
            )
            
            writer.write(b'\r\n')
            await writer.drain()
            
            banner = await asyncio.wait_for(reader.read(1024), timeout=timeout)
            writer.close()
            
            banner_text = banner.decode('utf-8', errors='ignore').strip()
            if banner_text:
                return banner_text[:200]
        except:
            pass
        return None
    
    async def scan_udp_port(self, port, semaphore, timeout=1):
        if not self.target_ip:
            return
        
        async with semaphore:
            try:
                if self.stealth_mode:
                    await asyncio.sleep(random.uniform(0.005, 0.02))
                
                loop = asyncio.get_running_loop()
                sock = await loop.run_in_executor(None, socket.socket, socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(timeout)
                
                try:
                    sock.sendto(b'\x00', (self.target_ip, port))
                    data = await loop.run_in_executor(None, sock.recvfrom, 1024)
                    if data:
                        service = self.udp_services.get(port, 'UNKNOWN')
                        self.udp_open_ports.append((port, service))
                        print(f"\n{C}[UDP] PORTA {port} ABERTA - {service}{W}")
                except:
                    pass
                finally:
                    sock.close()
            except:
                pass
    
    async def scan_port(self, port, semaphore, timeout=0.2):
        if not self.target_ip:
            return
        
        async with semaphore:
            try:
                if self.stealth_mode:
                    await asyncio.sleep(random.uniform(0.001, 0.01))
                
                loop = asyncio.get_running_loop()
                sock = await loop.run_in_executor(None, socket.socket, socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                
                try:
                    result = await loop.run_in_executor(
                        None,
                        lambda: sock.connect_ex((self.target_ip, port))
                    )
                    
                    if result == 0:
                        service = self.services.get(port, 'UNKNOWN')
                        banner = await self.grab_banner(port)
                        self.open_ports.append((port, service))
                        
                        if banner:
                            self.service_versions[port] = banner
                            print(f"\n{G}[+] PORTA {port} ABERTA - {service}{W}")
                            print(f"{Y}    📜 Banner: {banner[:100]}{W}")
                        else:
                            print(f"\n{G}[+] PORTA {port} ABERTA - {service}{W}")
                        
                        if port in self.vulnerable_ports:
                            print(f"{R}    ⚠️ VULN: {self.vulnerable_ports[port]}{W}")
                except:
                    pass
                finally:
                    sock.close()
            except:
                pass
    
    def detect_firewall(self):
        firewall_signs = []
        
        if len(self.open_ports) < 3 and self.total_ports > 1000:
            firewall_signs.append("Poucas portas abertas - possível firewall")
        
        if 22 in [p for p, _ in self.open_ports] and 80 not in [p for p, _ in self.open_ports]:
            firewall_signs.append("SSH aberto mas HTTP bloqueado - firewall detectado")
        
        if 443 in [p for p, _ in self.open_ports] and 80 not in [p for p, _ in self.open_ports]:
            firewall_signs.append("HTTPS aberto mas HTTP bloqueado - WAF possivelmente presente")
        
        if firewall_signs:
            self.firewall_detected = True
            print(f"\n{Y}[!] FIREWALL DETECTADO:{W}")
            for sign in firewall_signs:
                print(f"    🔥 {sign}")
    
    async def scan_range(self, start_port, end_port, timeout=0.2):
        semaphore = asyncio.Semaphore(self.max_concurrent)
        tasks = []
        
        for port in range(start_port, end_port + 1):
            task = asyncio.create_task(self.scan_port(port, semaphore, timeout))
            tasks.append(task)
            
            if len(tasks) >= self.max_concurrent:
                await asyncio.gather(*tasks)
                tasks = []
        
        if tasks:
            await asyncio.gather(*tasks)
    
    async def scan_udp_range(self, udp_ports, timeout=1):
        print(f"\n{C}[*] Escaneando portas UDP...{W}")
        semaphore = asyncio.Semaphore(1000)
        tasks = []
        
        for port in udp_ports:
            task = asyncio.create_task(self.scan_udp_port(port, semaphore, timeout))
            tasks.append(task)
            
            if len(tasks) >= 1000:
                await asyncio.gather(*tasks)
                tasks = []
        
        if tasks:
            await asyncio.gather(*tasks)
    
    async def scan_all(self):
        if not self.target_ip:
            print(f"{R}[!] Alvo inválido, abortando scan{W}")
            return
        
        self.start_time = time.time()
        
        print(f"\n{C}{'='*60}{W}")
        print(f"{C}🎯 Alvo: {self.original_target}{W}")
        print(f"{C}🔍 IP: {self.target_ip}{W}")
        print(f"{C}🔌 Total portas: {self.total_ports}{W}")
        print(f"{C}⚡ Threads: {self.max_concurrent}{W}")
        print(f"{C}🎭 Stealth: ATIVADO{W}")
        print(f"{C}{'='*60}{W}\n")
        
        # Portas comuns (prioridade máxima)
        common_ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,465,587,636,993,995,
                        1433,1521,1723,3306,3389,5432,5900,5901,6379,8080,8443,27017]
        
        print(f"{C}[*] Escaneando portas comuns (prioridade)...{W}")
        semaphore = asyncio.Semaphore(500)
        tasks = []
        for port in common_ports:
            task = asyncio.create_task(self.scan_port(port, semaphore, 0.15))
            tasks.append(task)
        await asyncio.gather(*tasks)
        
        # Escaneamento completo em chunks
        chunk_size = 10000
        for start in range(1, self.total_ports + 1, chunk_size):
            end = min(start + chunk_size - 1, self.total_ports)
            if start < 10000:
                continue
            
            await self.scan_range(start, end, 0.2)
            self.scan_progress = (end / self.total_ports) * 100
            print(f"{Y}[*] Progresso TCP: {self.scan_progress:.1f}% ({end}/{self.total_ports}){W}")
        
        # UDP
        udp_ports = [53, 67, 68, 69, 123, 161, 162, 514, 520]
        await self.scan_udp_range(udp_ports, 0.5)
        
        self.end_time = time.time()
        self.detect_firewall()
        self.generate_report()
    
    def generate_html_report(self):
        """Gera relatório HTML com gráficos"""
        elapsed = self.end_time - self.start_time if self.end_time else 0
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>yRecon - Scan Report</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: monospace; background: #ffffff; color: #0f0; margin: 20px; }}
        h1, h2 {{ color: #ff4444; }}
        .port-open {{ color: #00ff00; }}
        .port-closed {{ color: #ff4444; }}
        .vuln {{ color: #ffaa00; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
        th {{ background: #1a1a1a; }}
    </style>
</head>
<body>
    <h1>🔍 yRecon - MPScanner V1.0</h1>
    <h2>Relatório de Scan</h2>
    
    <h3>📊 Informações Gerais</h3>
    <table>
        <tr><th>Alvo</th><td>{self.original_target}</td></tr>
        <tr><th>IP</th><td>{self.target_ip}</td></tr>
        <tr><th>Data</th><td>{datetime.now()}</td></tr>
        <tr><th>Tempo</th><td>{elapsed:.2f} segundos</td></tr>
        <tr><th>Portas Abertas</th><td>{len(self.open_ports)}</td></tr>
        <tr><th>Firewall</th><td>{'DETECTADO' if self.firewall_detected else 'NÃO DETECTADO'}</td></tr>
    </table>
    
    <h3>🔓 Portas Abertas</h3>
    <table>
        <tr><th>Porta</th><th>Serviço</th><th>Banner</th><th>Vulnerabilidade</th></tr>
"""
        for port, service in sorted(self.open_ports):
            banner = self.service_versions.get(port, '-')[:50]
            vuln = self.vulnerable_ports.get(port, '-')
            vuln_class = 'vuln' if vuln != '-' else ''
            html += f"""        <tr><td class="port-open">{port}</td>
            <td>{service}</td>
            <td>{banner}</td>
            <td class="{vuln_class}">{vuln}</td></tr>
"""
        
        html += """    </table>
</body>
</html>"""
        
        filename = f"scan_{self.target_host.replace('.', '_')}.html"
        with open(filename, 'w') as f:
            f.write(html)
        print(f"{G}[+] HTML salvo: {filename}{W}")
    
    def generate_csv_report(self):
        """Gera relatório CSV"""
        filename = f"scan_{self.target_host.replace('.', '_')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Porta', 'Serviço', 'Banner', 'Vulnerável'])
            for port, service in sorted(self.open_ports):
                banner = self.service_versions.get(port, '')
                vuln = self.vulnerable_ports.get(port, '')
                writer.writerow([port, service, banner, vuln])
        print(f"{G}[+] CSV salvo: {filename}{W}")
    
    def generate_report(self):
        elapsed = self.end_time - self.start_time if self.end_time else 0
        
        print(f"\n{G}{'='*60}{W}")
        print(f"{G}📊 RELATÓRIO FINAL{W}")
        print(f"{G}{'='*60}{W}")
        print(f"{C}📍 Alvo: {self.original_target}{W}")
        print(f"{C}🔍 IP: {self.target_ip}{W}")
        print(f"{C}⏱️  Tempo: {elapsed:.2f}s{W}")
        print(f"{C}🔌 Portas TCP abertas: {len(self.open_ports)}{W}")
        print(f"{C}📡 Portas UDP abertas: {len(self.udp_open_ports)}{W}")
        print(f"{C}🛡️ Firewall: {'DETECTADO' if self.firewall_detected else 'NÃO DETECTADO'}{W}")
        
        if self.open_ports:
            print(f"\n{G}✅ PORTAS TCP ABERTAS:{W}")
            for port, service in sorted(self.open_ports):
                vuln = self.vulnerable_ports.get(port)
                vuln_mark = f"{R} [VULN: {vuln}]{W}" if vuln else ""
                print(f"   {G}🔓 {port:5d} - {service}{vuln_mark}{W}")
                if port in self.service_versions:
                    print(f"   {Y}      📜 {self.service_versions[port][:100]}{W}")
        
        if self.udp_open_ports:
            print(f"\n{C}✅ PORTAS UDP ABERTAS:{W}")
            for port, service in sorted(self.udp_open_ports):
                print(f"   {C}📡 {port:5d} - {service}{W}")
        
        # Exporta todos os formatos
        report_data = {
            'target': self.original_target,
            'ip': self.target_ip,
            'timestamp': datetime.now().isoformat(),
            'scan_time': elapsed,
            'tcp_ports': [{'port': p, 'service': s} for p, s in self.open_ports],
            'udp_ports': [{'port': p, 'service': s} for p, s in self.udp_open_ports],
            'service_versions': self.service_versions,
            'firewall_detected': self.firewall_detected,
            'vulnerabilities': {p: self.vulnerable_ports.get(p) for p, _ in self.open_ports if p in self.vulnerable_ports}
        }
        
        with open(f'scan_{self.target_host.replace(".", "_")}.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        print(f"\n{G}[+] JSON salvo: scan_{self.target_host.replace('.', '_')}.json{W}")
        
        self.generate_csv_report()
        self.generate_html_report()

async def main():
    print_banner()
    
    print(f"{Y}⚠️ Use apenas em servidores autorizados!{W}\n")
    
    target = input(f"{C}[?] IP / Domínio / URL: {W}")
    
    scanner = MPScannerV1(target)
    await scanner.scan_all()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrompido{W}")
    except Exception as e:
        print(f"\n{R}[!] Erro: {e}{W}")
