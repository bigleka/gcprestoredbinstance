GCP Restore Tool

   Uma ferramenta gráfica simples, para ajudar na restauração de backups de instâncias do Google Cloud SQL entre projetos.
   Caso você precise voltar no tempo, restaurar pontualmente um banco, ou provar para a auditoria que o backup funciona
   e não quer e não pode restaurar por cima do ambiente atual, ou precisa restaurar em um outro projeto para qualquer outra situação.

🚀 Características

   Interface gráfica fácil de usar construída com Tkinter.
   Seleção de projeto e instância de origem através de dropdowns.
   Visualização de backups disponíveis para a instância selecionada.
   Seleção de projeto e instância de destino através de dropdowns.
   Execução da operação de restauração com apenas um clique.

📸 Screenshot

![image](https://github.com/bigleka/gcprestoredbinstance/assets/13354954/399b48ac-f955-4953-9a06-2f52b19c45f5)


🛠 Instalação
1. Clone o repositório:
   git clone https://github.com/bigleka/gcprestoredbinstance

2. Instale as dependências
   
   pip install google-auth google-auth-oauthlib
   
   pip install --upgrade google-api-python-client 

3. Instale o GCP client para seu SO.
   
4. Gere as credencias necessárias da GCP usando o comando

   gcloud auth application-default login

   Ele deve redirecionar você para a tela de logon da sua conta do GCP, após logar,
   volte para a linha de comando e veja onde ele gerou o arquivo "application_default_credentials.json"

5. Execute o script:
   python gcp_restore_cloud_database_in_other_project.py

⚙ Uso
   
   Carregue seu arquivo de credenciais do GCP.
   
   Selecione o projeto e a instância de origem.
   
   Clique em "Load Backups" para listar os backups disponíveis.
   
   Selecione o projeto e a instância de destino.
   
   Clique em "Restore" para iniciar o processo de restauração.

ATENÇÃO !!!
   
   Para executar esta operação, você precisa criar uma instância do Google Cloud SQL dentro do projeto de destino.
   
   Esse processo vai sobreescrever completamente a instância de destino !!!

🙏 Contribuições
   
   Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir uma issue ou pull request.
