# DOCs: http://docs.paramiko.org/en/2.6/api/sftp.html
#str.replace(stt,cng)
#DEPENDENCIAS PARA EXECUÇÃO
import paramiko 
from datetime import datetime, timedelta
import pyscreenshot as ImageGrab
import os

#
def baixa_arquivos(filial, arquivos):

    if( len(arquivos) == 0):
        return False;

    print("Baixando Arquivos de",filial , "...")
    print("arquivos:",arquivos)

#TAMANHO DA JANELA
cmd = 'mode 50,20'
os.system(cmd)
#Credenciais para acessar o servidor e listar os arquivos
URL   =  '#####'
User  =  '#####'
Pass  =  '######'
ssh = paramiko.SSHClient()

#data
dt = datetime.today() - timedelta(hours=8)
data = dt.strftime("%d%m%y")
data_dm = dt.strftime("%d%m")

#Uma string com todos os arquivos para listagem
Arquivos_receber = "agenda."+ data_dm + "*" + " ba241111" + data + "*" + " cm241111" + data + "*" + " ms030" + data + "*" + " sc241111" + data + "*" + " cpr111" + data + "*" + " fn" + data + "*" + " it241111" + data + "*" + " it241008" + data + "*" + " it241180" + data + "*" + " it241181" + data + "*" + " it241183" + data + "*" + " me000" + data + "*" + " pa241" + data + "*" + " pc241111" + data + "*" + " pc241030" + data + "*" + " pc241180" + data + "*" + " pc241181" + data + "*" + " prf241180" + data + "*" + " lms030" + data + "*" + " lbm111" + data + "*" + " pd241111" + data + "*" + " pd241030" + data + "*" + " pd241063" + data + "*" + " pd241180" + data + "*" + " pd241181" + data + "*" + " ca111" + data + "*" + " tb030" + data + "*" + " pf000" + data + "*" + " ef000" + data + "*" + " set111" + data + "*" + " ucl111" + data + ".txt* cmc241111_" + data + "_" + data + "*" + ""

# Um vetor para cada filial
Arquivos_Matriz_vet = ("agenda."+ data_dm +  " ba241111" + data +  " cm241111" + data +  " sc241111" + data +  " cpr111" + data +  " fn" + data +  " it241111" + data +  " it241008" + data +  " me000" + data +  " pa241" + data +  " pc241111" + data +  " lbm111" + data + ".dat" +" pd241111" + data +  " pd241063" + data +  " ca111" + data +  " pf000" + data +  " ef000" + data +  " set111" + data + ".txt"+ " ucl111" + data + ".txt cmc241111_" + data + "_" + data + ".txt").split(" ")
Arquivos_030_vet = ("ms030" + data + " lms030" + data + ".dat"+  " pc241030" + data +  " pd241030" + data +   " tb030" + data).split(" ")
Arquivos_180_vet = ("it241180" + data +  " pc241180" + data +  " prf241180" + data +  " pd241180" + data).split(" ")
Arquivos_181_vet = ("it241181" + data +  " pc241181" + data +  " pd241181" + data).split(" ") 
Arquivos_183_vet = ("it241183" + data).split(" ")

#Adiciona chaves automaticamente, brabo d+ 
ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

#Abre a conexao
ssh.connect(URL, username=User, password=Pass)
ftp = ssh.open_sftp()
 
# Retorna somente os arquivos já Baixados 
command = 'cd /fs1/integra/ ; ls ' + Arquivos_receber
(stdin, stdout, stderr) = ssh.exec_command(command)
 
#Aqui itera nos arquivos baixados e remove os já baixados de cada vetor
for line in stdout.readlines():
    line = line.replace('\n', '') 
    if( line in Arquivos_Matriz_vet):
        Arquivos_Matriz_vet.remove(line)

    if( line in Arquivos_030_vet):
        Arquivos_030_vet.remove(line)

    if( line in Arquivos_180_vet):
        Arquivos_180_vet.remove(line)

    if( line in Arquivos_181_vet):
        Arquivos_181_vet.remove(line)

    #print(line)
    


#
print("Arquivos Faltantes da Matriz:",Arquivos_Matriz_vet)
print("Arquivos Faltantes da 030:",Arquivos_030_vet)
print("Arquivos Faltantes da 180:",Arquivos_180_vet)
print("Arquivos Faltantes da 181:",Arquivos_181_vet)
print("Arquivos Faltantes da 183:",Arquivos_183_vet)

#
baixa_arquivos("srvsave",Arquivos_Matriz_vet)
baixa_arquivos("srvsave030",Arquivos_030_vet)
baixa_arquivos("srvsave180",Arquivos_180_vet)
baixa_arquivos("srvsave181",Arquivos_181_vet)
baixa_arquivos("srvsave183",Arquivos_183_vet)
 
ssh.close()