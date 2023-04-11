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

    ###########################################################################################
    # Put File to Host (SFTP)
    # srcFilePath: Local(PC, client), desFilePath: Server(host)
    def putFromHost(self, srcFilePath, dstFilePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.put(srcFilePath, dstFilePath)

    ###########################################################################################
    # Rename file on Host (SFTP)
    # srcFilePath: Old Name, desFilePath: New Name
    def renameHostFile(self, srcFilePath, dstFilePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.rename(srcFilePath, dstFilePath)

    ###########################################################################################
    # Delete file on Host (SFTP)
    # filePath: Server(host)
    def deleteHostFile(self, filePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        self.ftp_client.remove(filePath)

    ###########################################################################################
    # Get file list on Host (SFTP)
    # filePath: Server(host)
    def getFileListFromHost(self, filePath):
        # SFTP 객체를 생성하지 않았으면...(접속한적이 없으면)
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        return self.ftp_client.listdir(filePath)

    ######################################################################
    # Get file list of host
    # srcFilePath: Server(host)
    def getFileAttrListFromHost(self, srcFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()
        return self.ftp_client.listdir_attr(srcFilePath)

    ######################################################################
    # Delete folder of host
    # srcFilePath: Server(host)
    def deleteHostFolder(self, srcFilePath):
        if self.ftp_client is None:
            # Get SFTP object from SSHClient
            self.ftp_client = self.client.open_sftp()

        # # Only current folder only
        # file_list = self.getFileListFromHost(srcFilePath)
        # for file in file_list:
        #     file_path = os.path.join(srcFilePath, file)  # srcFilePath /var/www  filename: log.txt -> /var/www/log.txt
        #     file_path = file_path.replace('\\', '/')
        #     self.deleteHostFile(file_path)

        # Delete all subflder recursive
        file_attr_list = self.ftp_client.listdir_attr(srcFilePath)
        for file_attr in file_attr_list:
            path = os.path.join(srcFilePath, file_attr.filename)
            path = path.replace('\\', '/')
            # Path is Folder type
            if stat.S_ISDIR(file_attr.st_mode):
                self.deleteHostFolder(path)
            # Path is File type
            else:
                self.deleteHostFile(path)

        self.ftp_client.rmdir(srcFilePath)

    ############################################################################################################################################

    ######################################################################
    # Get file from host with SCP
    # srcFilePath: Server(host) dstFilePath: Local(PC, client)
    def getFromHostWithSCP(self, srcFilePath, desFilePath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.get(srcFilePath, desFilePath)

    ######################################################################
    # Put file to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    def putToHostWithSCP(self, srcFilePath, dstFilePath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.put(srcFilePath, dstFilePath)

    ######################################################################
    # Put folder to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    def putFolderToHostSCP(self, srcDirPath, dstDirPath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.put(srcDirPath, dstDirPath, recursive=True)

    ######################################################################
    # Get folder to host with SCP
    # srcFilePath: Local(PC, client) dstFilePath: Server(host)
    def getFolderToHostSCP(self, srcDirPath, dstDirPath):
        if self.scp_client == None:
            self.scp_client = SCPClient(self.client.get_transport())
        self.scp_client.get(srcDirPath, dstDirPath, recursive=True)

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
            # ssh.getFromHost('./process_list.txt', 'process_list.txt')

            ################################################################################
            # 서버로 파일 업로드
            # ssh.putFromHost('lec_paramiko.py', 'lec_paramiko.py')

            ################################################################################
            # 서버에 있는 파일명 변경
            # ssh.renameHostFile('./process_list.txt', './process.txt')
            # ssh.renameHostFile('./temp', './temp2')

            ################################################################################
            # 서버에 있는 파일삭제
            # ssh.deleteHostFile('./process_list.txt')

            ################################################################################
            # 서버의 폴더내 파일목록 가져오기
            # file_list = ssh.getFileListFromHost('./temp')
            # print(file_list)
            # for file in file_list:
            #     print(file)

            ################################################################################
            # 서버의 폴더내 파일목록을 속성과 함께 가져오기
            # file_list = ssh.getFileAttrListFromHost('./temp')
            # print(file_list)
            # for file in file_list:
            #     print(file)

            ################################################################################
            # 서버의 폴더삭제
            # ssh.deleteHostFolder('./temp')

            ######################################################################
            # Get file from host with scp
            # ssh.getFromHostWithSCP('./process_list.txt', 'process_list.txt')

            ######################################################################
            # Put file to host with scp
            # ssh.putToHostWithSCP('./process_list.txt', 'process_list.txt')

            ######################################################################
            # Get folder from host with scp
            # ssh.getFolderToHostSCP('temp', 'temp')

            ######################################################################
            # Put folder to host with scp
            # ssh.putFolderToHostSCP('temp', 'temp')

        else:
            print('Connect is failed!!!')

    except Exception as e:
        print(e)






































