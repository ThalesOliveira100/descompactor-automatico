# 📦 Descompactador Automático de Arquivos com Redirecionamento em Pastas Específicas

Este projeto é um **script Python que monitora continuamente uma pasta específica no Windows**. Sempre que um novo arquivo compactado é adicionado (nos formatos `.zip`, `.rar` ou `.7z`), o script o descompacta e distribui os arquivos internos para diretórios pré-definidos, além de registrar logs com horário e ID da demanda, agilizando o fluxo de testes manuais do sistema.


---


## 🚀 Funcionalidades

- Monitora automaticamente uma pasta de entrada (`C:/TESTES`)  
- Detecta novos arquivos `.zip`, `.rar`, ou `.7z`  
- Descompacta o conteúdo automaticamente  
- Move os arquivos extraídos para diretórios específicos:  
  - `DYGNUS.EXE`, `DYGNUS_START.EXE`, `DYGNUS_UPDATE.EXE` → `C:\MULT\DYGNUS`
  - `DYGNUS.EXE` + `DYGNUS_UPDATE.EXE` → `C:\MULT\DYGNUS\SETUP\APP`
  - `DYGNUS_START.EXE` → `C:\MULT\DYGNUS\SETUP`
  - Se houver `PDVLINE.EXE`, também é movido para `C:\MULT\PDV` e `C:\MULT\DYGNUS\SETUP\APP`
  - Se houver `PDV_NFCE_SAT.EXE`, será movido para `C:\MULT\PDV`
  - Se houver `NFE.EXE`, também é movido para `C:\MULT\NFE`
  - Se houver `DYGNUS_ETIQUETAS.EXE`, `DYGNUS_WAVES_ECOMMERCE_ONE.EXE`, `DYGNUS_WOO.EXE` ou `DYGNUS-WAVE.EXE`, estes serão movidos para `C:\MULT\DYGNUS` e para `C:\MULT\DYGNUS\SETUP\APP`
- Registra logs dos arquivos descompactoes em `LOG_TESTES.txt` e em caso de erros no arquivo `LOG_ERRO.txt`. Estes arquivos são salvos dentro da pasta `C:/TESTES` e são editados sempre que é necessário armazenar um novo log, assim, a informação salva antes não será sobrescrita.
- Exibe notificações toast (a notificação do Windows) durante as etapas do script, incluindo em casos de erro na descompactação  
- Remove o arquivo compactado da pasta `C:/TESTES` após redirecionar cada executável para sua pasta de destino
- Roda de forma contínua em background (sem terminal visível)


---


## 📂 Estrutura Esperada do Arquivo Compactado

- Nome padrão: `0011758 - DYGNUS.zip`  
  (O número no início, identificador da demanda, será usado como ID no log)
  
- Arquivos esperados dentro:
  - `DYGNUS.EXE`
  - `DYGNUS_START.EXE`
  - `DYGNUS_UPDATE.EXE`
  - `PDVLINE.EXE`
  - `PDV_NFCE_SAT.EXE`
  - `NFE.EXE`
  - `DYGNUS_ETIQUETAS.EXE`
  - `DYGNUS_WAVES_ECOMMERCE_ONE.EXE`
  - `DYGNUS_WOO.EXE`
  - `DYGNUS-WAVE.EXE`


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
      │    ├── DYGNUS_UPDATE.EXE
      |    ├── DYGNUS_ETIQUETAS.7z (se presente)
      |    ├── DYGNUS_WAVES_ECOMMERCE_ONE.7z (se presente)
      |    ├── DYGNUS_WOO.7z (se presente)
      |    └── DYGNUS-WAVE.7z (se presente)
      ├── DYGNUS\
      │    └── SETUP\
      │         ├── DYGNUS_START.EXE
      │         └── APP\
      │              ├── DYGNUS.EXE
      │              ├── DYGNUS_UPDATE.EXE
      |              ├── DYGNUS_ETIQUETAS.7z (se presente)
      |              ├── DYGNUS_WAVES_ECOMMERCE_ONE.7z (se presente)
      |              ├── DYGNUS_WOO.7z (se presente)
      |              |── DYGNUS-WAVE.7z (se presente)
      │              └── PDVLINE.EXE (se presente)
      └── PDV\
           |── PDV_NFCE_SAT.EXE (se presente)
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

* O script oferece suporte para arquivos sem o número/identificador da demanda no início do nome (exemplo: DYGNUS_ETIQUETAS.7z, DYGNUS_WAVES_ECOMMERCE_ONE.7z, DYGNUS_WOO.7z e DYGNUS-WAVE.7z)
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
🔗 [linkedin.com/in/devthalesoliveira](https://www.linkedin.com/in/devthalesoliveira)  
📧 [toliveiradev@outlook.com](mailto:toliveiradev@outlook.com)  


---


## 📄 Licença

Este projeto está licenciado sob a Licença MIT.
