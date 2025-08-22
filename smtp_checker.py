import smtplib
import dns.resolver
import socket
from typing import List, Dict
from config import Config
import time

def get_smtp_hosts(domain: str) -> List[str]:
    """Generate potential SMTP hosts for a domain"""
    base_hosts = [
        f'smtp.{domain}',
        f'mail.{domain}',
        f'smtp1.{domain}',
        f'smtp2.{domain}',
        f'email.{domain}',
        f'mailin.{domain}',
        f'mx.{domain}',
        domain
    ]
    
    # Get MX records
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        base_hosts.extend(str(r.exchange).rstrip('.') for r in mx_records)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        pass
    
    return list(set(base_hosts))

def test_smtp_connection(host: str, port: int, encryption: str) -> bool:
    """Test if host:port accepts SMTP connections"""
    try:
        if encryption == 'ssl':
            with smtplib.SMTP_SSL(host, port, timeout=5) as server:  # Reduced timeout
                return True
        else:
            with smtplib.SMTP(host, port, timeout=5) as server:  # Reduced timeout
                if encryption == 'starttls':
                    server.starttls()
                return True
    except (smtplib.SMTPException, socket.timeout, ConnectionRefusedError, OSError):
        return False

def authenticate_smtp(host: str, port: int, email: str, password: str, encryption: str) -> bool:
    """Perform actual SMTP authentication"""
    try:
        if encryption == 'ssl':
            with smtplib.SMTP_SSL(host, port, timeout=10) as server:
                server.login(email, password)
                return True
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                if encryption == 'starttls':
                    server.starttls()
                server.login(email, password)
                return True
    except smtplib.SMTPAuthenticationError:
        return False
    except (smtplib.SMTPException, socket.timeout, ConnectionRefusedError):
        return False

def detect_smtp_config(email: str, password: str) -> Dict:
    """Main detection workflow"""
    domain = email.split('@')[-1]
    hosts = get_smtp_hosts(domain)
    
    # Test ports in order of preference
    port_configs = [
        (587, 'starttls'),
        (465, 'ssl'),
        (2525, 'starttls'),
        (25, 'none')
    ]
    
    for host in hosts:
        for port, encryption in port_configs:
            if test_smtp_connection(host, port, encryption):
                if authenticate_smtp(host, port, email, password, encryption):
                    return {
                        'email': email,
                        'password': password,
                        'host': host,
                        'port': port,
                        'encryption': encryption,
                        'valid': True
                    }
                # Small delay to avoid rate limiting
                time.sleep(0.1)
    
    return {
        'email': email,
        'password': password,
        'host': None,
        'port': None,
        'encryption': None,
        'valid': False
    }

def process_email_list(emails: List[str]) -> List[Dict]:
    """Process batch of email:password combinations"""
    results = []
    for line in emails:
        if ':' in line:
            email, password = line.split(':', 1)
            results.append(detect_smtp_config(email.strip(), password.strip()))
    return results