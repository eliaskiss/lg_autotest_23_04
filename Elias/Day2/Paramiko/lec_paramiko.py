import paramiko
from paramiko import SSHClient
from scp import SCPClient
import os
import stat

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
    # Disconnect
    ##############################################################
    def disconnect(self):
        pass

if __name__ == '__main__':
    ssh = MySSH()

    try:
        if ssh.connet('117.52.91.88', 'elias', '1111', timeout=5, port=22):
            print('SSH is connected')

            ##############################################################
            # Process List 파일생성(ps -ef > process_list.txt)
            ##############################################################
            ssh.exeCommand('ps -ef > process_list.txt', False)

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

            for file in ssh.exeCommand('cd temp && ls -al&& pwd', True):
                print(file, end='')


        else:
            print('Connect is failed!!!')

    except Exception as e:
        print(e)






































