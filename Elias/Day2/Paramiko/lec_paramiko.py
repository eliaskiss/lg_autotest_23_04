import paramiko
from paramiko import SSHClient
from scp import SCPClient
import os
import stat
import time

class MySSH:
    def __init__(self):
        self.ftp_client = None  # SFTP
        self.client = None      # SSH
        self.scp_client = None  # SCP

    ##############################################################
    # Connect Host
    ##############################################################
    # todo: SSH로 서버에 연결하는 함수작성필요
    def connet(self, host, user_id, user_password, port=22, timeout=None):
        # 접속한 상태가 아니면
        if self.client is None:
            self.client = SSHClient()
            # 이코드가 없으면 'Sever ... ' not found in known hosts 에러발생
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=host, port=port, username=user_id, password=user_password, timeout=timeout)

            if self.isAlive():
                self.password = user_password
                return True
            else:
                return False

    ##############################################################
    # Check Connection
    ##############################################################
    def isAlive(self):
        if self.client is None:
            return None
        else:
            return self.client.get_transport().is_active()

    ##############################################################
    # Execute Shell Command
    ##############################################################
    def exeCommand(self, command, isReturn = False):
        if self.isAlive():
            # _, stdout, _ = self.client.exec_command(command)
            stdin, stdout, stderr = self.client.exec_command(command)

            if isReturn is True:
                return stdout.readlines()

        else:
            print('Client is not connected!!!')

    ##############################################################
    # Execute Shell Command
    ##############################################################
    def exeCommand(self, command, isReturn=False):
        if self.isAlive():
            # _, stdout, _ = self.client.exec_command(command)
            stdin, stdout, stderr = self.client.exec_command(command)

            if isReturn is True:
                return stdout.readlines()

        else:
            print('Client is not connected!!!')

    ##############################################################
    # Execute Shell Command as root
    ##############################################################
    def sudoCommand(self, command, isReturn=False):
        if self.isAlive():
            stdin, stdout, stderr = self.client.exec_command('sudo ' + command, get_pty=True)

            stdin.write(self.password + '\n')
            stdin.flush()
            time.sleep(0.1)

            if isReturn is True:
                return stdout.readlines()

        else:
            print('Client is not connected!!!')

    ##############################################################
    # Disconnect
    ##############################################################
    def disconnect(self):
        pass

    ##############################################################
    # Get File from Host (SFTP)
    # scrFilePath: Server(host), desFilePath: Local(PC, Client)
    ##############################################################
    def getFromHost(self, srcFilePath, dstFilePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.get(srcFilePath, dstFilePath)


if __name__ == '__main__':
    ssh = MySSH()

    try:
        if ssh.connet('117.52.91.88', 'elias', '1111', timeout=5, port=22):
            print('SSH is connected')

            ##############################################################
            # Process List 파일생성(ps -ef > process_list.txt)
            ##############################################################
            # ssh.exeCommand('ps -ef > process_list.txt', False)

            ##############################################################
            # 파일목록 가져오기 (ls -al)
            ##############################################################
            # file_list = ssh.exeCommand('ls -al', True)
            # for file in file_list:
            #     print(file, end='')

            ##############################################################
            # temp 폴더생성 (putty)
            # > mkdir temp
            # process_list.txt 파일생성 (putty)
            # > cd temp
            # > ps -ef > process_list.txt
            # Python Code
            # cd temp --> ls -al --> 파일목록 가져오기
            ##############################################################

            # ssh.exeCommand('cd temp')
            # for file in ssh.exeCommand('ls -al', True):
            #     print(file, end='')

            '''
            ; - 앞의 명령어가 실패해도 다음 명령어가 실행
            && - 앞의 명령어가 성공했을 때 다음 명령어가 실행
            & - 앞의 명령어를 백그라운드로 돌리고 동시에 뒤의 명령어를 실행
            https://opentutorials.org/module/2538/15818
            '''

            # for file in ssh.exeCommand('cd temp && ls -al&& pwd', True):
            #     print(file, end='')

            ##############################################################
            # 쉘 스크립트 파일 생성
            ##############################################################
            # ssh.exeCommand('echo "ps -ef > process_list.txt" > make_process_list.sh')
            # ssh.exeCommand('chmod 777 ./make_process_list.sh')

            ##############################################################
            # sudo 커맨드 실행
            ##############################################################
            # ssh.exeCommand('sudo mkdir /var/temp')
            # ssh.sudoCommand('mkdir /var/temp')

            ##############################################################
            # 서버로 부터 파일 가져오기
            ##############################################################
            ssh.getFromHost('./process_list.txt', 'process_list.txt')

        else:
            print('Connect is failed!!!')

    except Exception as e:
        print(e)






































