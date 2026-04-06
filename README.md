*SIEM Simples** é uma ferramenta leve, moderna e fácil de usar para monitorar ataques contra seu servidor Linux em tempo real.

---

## 🎯 Para que serve?

Esta aplicação foi criada para ajudar administradores e desenvolvedores a:

- Monitorar logs do sistema e da aplicação em tempo real
- Detectar tentativas de ataque (brute force SSH, falhas de autenticação, erros 4xx/5xx, etc.)
- Identificar o **IP** e o **país** de origem dos ataques
- Visualizar estatísticas claras (quantidade de ataques, IPs bloqueados, países atacando)
- **Bloquear IPs maliciosos com apenas 1 clique** usando `iptables`
- Ter um dashboard bonito e atualizado automaticamente

É ideal para VPS, servidores dedicados, aplicações web (Nginx, Apache, Node.js, Python, etc.).

---

## ✨ Funcionalidades

- Dashboard web moderno e responsivo
- Monitoramento automático de múltiplos logs
- Detecção inteligente de padrões de ataque
- Identificação automática de país usando IP-API
- Bloqueio automático de IPs via iptables
- Atualização em tempo real (a cada poucos segundos)
- Interface simples e intuitiva
- Fácil de adicionar novos logs da sua aplicação

---

## 🚀 Como instalar e usar

### Pré-requisitos
- Servidor Linux (Ubuntu, Debian, CentOS, etc.)
- Python 3.8 ou superior
- Permissões de root (necessário para ler logs do sistema e usar iptables)

### Passo a passo

1. **Clone o repositório** (ou baixe os arquivos):

```bash
git clone https://github.com/Charyflux/SIEMPoc.git
