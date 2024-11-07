<h1 align="center">
  <br>
  Programa Cloudflare DDNS
  <br>
</h1>

<h4 align="center">Um atualizador de DDNS para domínios Cloudflare usando Python, CustomTKinter e PyStray.</h4>

<p align="center">
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/blob/main/README.pt-br.md"><img alt="GitHub lang" src="https://img.shields.io/badge/lang-pt--br-green.svg"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/blob/main/README.md"><img alt="GitHub lang" src="https://img.shields.io/badge/lang-en-red.svg"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/commits/main/"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Matozo0/cloudflare-ddns-app"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Matozo0/cloudflare-ddns-app?style=for-the-badg"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/releases"><img alt="GitHub downloads" src="https://img.shields.io/github/downloads/Matozo0/cloudflare-ddns-app/latest/total"></a>
</p>

<p align="center">
  <a href="#recursos">Recursos</a> -
  <a href="#como-usar">Como Usar</a> -
  <a href="#baixar">Baixar</a> -
  <a href="#instalação">Instalação</a> -
  <a href="#licença">Licença</a>
</p>

## Recursos

- **Detecção Automática de IP**: Detecta e atualiza automaticamente seu endereço IP público em intervalos configuráveis.
- **Integração com API da Cloudflare**: Atualiza os registros DNS de forma segura utilizando a API da sua conta Cloudflare.
- **Configuração Simples**: Configuração fácil e local para maior flexibilidade e segurança.
- **Segurança Local**: Suas chaves de API e configurações de domínio permanecem protegidas no seu computador.
- **Suporte Multiplataforma**: Disponível como executável para Windows ou script em Python.
- **Controle de Erros e Notificações**: Notifica e gera logs para atualizações bem-sucedidas ou com falhas.
- **Atualização Manual**: Permite forçar atualizações instantâneas pelo ícone da bandeja do sistema.

## Como Usar

1. **Baixe o Executável**: Acesse a página de [Releases](https://github.com/Matozo0/cloudflare-ddns-app/releases) e baixe a versão mais recente para Windows.
2. **Rode o Executável**: Clique duas vezes no arquivo baixado para iniciar o aplicativo.
3. **Interaja com o Ícone da Bandeja**:
    - Clique com o botão esquerdo no ícone da bandeja para acessar as `Configurações`.
   - Clique com o botão direito no ícone da bandeja para acessar opções como `Configurações`, `Atualizar Agora` e `Sair`.

> **Nota**: As versões para Linux e MacOS estarão disponíveis em breve.

## Configuração Manual em Python

#### Pré-requisitos

- **Python 3.11+**
- **Conta Cloudflare** com acesso à Chave Global da API.
- **Dependências**: Listadas em `requirements.txt`

#### Instalação

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/Matozo0/cloudflare-ddns-app.git
   cd cloudflare-ddns-app
   ```

2. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a Aplicação**:
   ```bash
   python main.py
   ```

## Baixar

Para facilitar, você pode baixar o executável pré-compilado na página de [Releases](https://github.com/Matozo0/cloudflare-ddns-app/releases/).

## Licença

Este projeto é licenciado sob a Licença MIT.

---

> GitHub [@Matozo0](https://github.com/Matozo0)