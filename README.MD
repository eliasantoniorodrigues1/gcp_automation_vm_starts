# Automation GCP VM Start

Processo criado para automatizar a instalação de softwares ao iniciar a VM

---

### Scripts executados na criação da VM

        sudo su
        sudo apt update
        sudo apt install -yq software-properties-common
        sudo add-apt-repository -yq ppa:deadsnakes/ppa
        sudo  apt-get install -y python3.9 python3.9-dev python3.9-venv
        sudo apt-get install wget
        wget https://bootstrap.pypa.io/get-pip.py
        sudo python3 get-pip.py
        cd /home
        mkdir your-user
        gsutil cp -r gs://your-user/your-project-folder/ /home/your-user/
        cd /home/your-user/your-project-folder/your-projsect-sub-folder
        python3.9 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python3.9 main.py


 - Os passos acima fazem as seguintes ações:

# Primeiro Passo Criar um Bucket para armazenar a pasta do seu projeto

Não é necessário dizer que você precisa de ter acesso a um projeto e criar uma conta de serviço para poder 
executar as tarefas.

 1 - Troca de usuário para fazer todos os procesimentos com o super user root
 2 - Atualiza os pacotes do linux (sudo apt update, sudo apt install -yq software-properties-common)
 3 - Adiciona o repositório que contem a versão 3.9 do Python
 4 - Instala o PIP e o virtual Env
 5 - Copia os arquivos do bucket "bucket-que-armazena-seu-projeto" para a pasta /home/usuário da máquina criada
 6 - Cria o ambiente virtual do python
 7 - Ativa o ambiente virtual
 8 - Instala as dependencias do projeto que estão contidas em "requirements.txt"
 9 - Executa o script que roda as consultas no banco
 10 - Desliga a máquina para não gerar custos desnecessários

### Observações:

Essa VM está configurada para ficar ligada no máximo uma hora, tendo em vista que o processo
demora em média 10 minutos para executar completamente.

 -  Conta de serviço utilizada sua-conta-de-servico-google
 - Tempo máximo de execução da VM é de 1 hora após esse tempo a máquina é encerrada

