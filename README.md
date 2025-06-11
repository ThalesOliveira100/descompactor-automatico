# 📦 Descompactador Automático de Arquivos com Redirecionamento em Pastas Específicas

Este projeto é um **script Python que monitora continuamente uma pasta específica no Windows**. Sempre que um novo arquivo compactado é adicionado (nos formatos `.zip`, `.rar` ou `.7z`), o script o descompacta e distribui os arquivos internos para diretórios pré-definidos, além de registrar logs com horário e ID da demanda, agilizando o fluxo de testes manuais do sistema.


---


## 🚀 Funcionalidades

- 📁 Monitora automaticamente uma pasta de entrada (`C:/TESTES`)  
- 🔍 Detecta novos arquivos `.zip`, `.rar`, ou `.7z`  
- 🔓 Descompacta o conteúdo automaticamente  
- 📤 Move os arquivos extraídos para diretórios específicos:  
  - `DYGNUS.EXE`, `DYGNUS_START.EXE`, `DYGNUS_UPDATE.EXE` → `C:\MULT\DYGNUS`
  - `DYGNUS.EXE` + `DYGNUS_UPDATE.EXE` → `C:\MULT\DYGNUS\SETUP\APP`
  - `DYGNUS_START.EXE` → `C:\MULT\DYGNUS\SETUP`
  - Se houver `PDVLINE.EXE`, também é movido para `C:\MULT\PDV` e `C:\MULT\DYGNUS\SETUP\APP`
  - Se houver `NFE.EXE`, também é movido para `C:\MULT\NFE`
- 🗒️ Registra logs em `LOG_TESTES.txt` com horário e ID extraído do nome do arquivo, após descompactar um arquivo  
- 🗒️ Registra logs em `LOG_ERRO.txt` com horário e ID extraído do nome do arquivo, em casos de erro  
- 🔔 Exibe notificações toast durante as etapas do script  
- 🧼 Remove o arquivo compactado após processar  
- 🔁 Roda de forma contínua em background  


---


## 📂 Estrutura Esperada do Arquivo Compactado

- Nome padrão: `0011758 - DYGNUS.zip`  
  (O número no início, identificador da demanda, será usado como ID no log)
  
- Arquivos esperados dentro:
  - `DYGNUS.EXE`
  - `DYGNUS_START.EXE`
  - `DYGNUS_UPDATE.EXE`
  - `PDVLINE.EXE` (opcional)
  - `NFE.EXE` (opcional)


---


## 🧱 Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [`watchdog`](https://pypi.org/project/watchdog/) — para monitorar o sistema de arquivos
- [`zipfile`](https://docs.python.org/3/library/zipfile.html) — descompactação nativa de `.zip`
- [`py7zr`](https://pypi.org/project/py7zr/) — descompactação de arquivos `.7z`
- [`rarfile`](https://pypi.org/project/rarfile/) — descompactação de arquivos `.rar` (requer [`unrar.exe`](https://www.rarlab.com/rar_add.htm))
- [`plyer`](https://pypi.org/project/plyer/) — para notificações no Windows


---


## 🛠️ Como usar

### 1. Clone este repositório

```bash
git clone https://github.com/thalesoliveira100/descompactador-automatico.git
cd descompactador-automatico
```

### 2. Instale as dependências

> ⚠️ Certifique-se de que o `unrar.exe` esteja disponível no PATH ou na mesma pasta do script.

```bash
pip install -r requirements.txt
```

### 3. Execute o script

```bash
python descompactador.py
```

> O script iniciará a escuta da pasta `C:\TESTES` (criando a pasta caso não exista) e começará a operar automaticamente.


---


## 📑 Estrutura de diretórios de destino

```
C:\
 └── MULT\
      ├── DYGNUS\
      │    ├── DYGNUS.EXE
      │    ├── DYGNUS_START.EXE
      │    └── DYGNUS_UPDATE.EXE
      ├── DYGNUS\
      │    └── SETUP\
      │         ├── DYGNUS_START.EXE
      │         └── APP\
      │              ├── DYGNUS.EXE
      │              ├── DYGNUS_UPDATE.EXE
      │              └── PDVLINE.EXE (se presente)
      └── PDV\
           └── PDVLINE.EXE (se presente)
      └── NFE\
           └── NFE.EXE (se presente)
```


---


## 🪵 Exemplo de log gerado (`LOG_TESTES.txt`)

```
[0011841: "(nome da demanda)"](https://mantis.multilogica.com.br/view.php?id=0011841) 14:32
```


---


## ⚠️ Observações

* Arquivos com os nomes [`DYGNUS.7Z`, `DYGNUS_ETIQUETAS.7z`, `DYGNUS_WAVES_ECOMMERCE_ONE.7z`, `DYGNUS_WOO.7z`, `DYGNUS-WAVE.7z`, `NFE.7z`, `PDVLINE.7z`] **são ignorados** propositalmente por não serem gerados no formato ideal "[numero da demanda] - [nome do sistema]".
* Em caso de erro ao mover os arquivos (ex: `arquivo em uso`), o erro é notificado via `toast` (a notificação do Windows) e registrado no arquivo LOG_ERROS.txt.
* O script pode ser adicionado à **pasta de inicialização do Windows** ou ser executado via `Task Scheduler` para iniciar com o sistema.


---


## 💡 Possíveis melhorias futuras

* Interface gráfica para ativar/desativar o monitoramento
* Consulta no Mantis BugTracker para obter o título da demanda, e seu registro no arquivo LOG_TESTES.txt
* Dashboard para visualizar logs em tempo real
* Envio de notificações por email


---


## 👤 Autor

**Thales Oliveira**  
🔗 [linkedin.com/in/seu-usuario](https://www.linkedin.com/in/devthalesoliveira)  
📧 [toliveiradev@outlook.com](mailto:toliveiradev@outlook.com)  


---


## 📄 Licença

Este projeto está licenciado sob a Licença MIT.
