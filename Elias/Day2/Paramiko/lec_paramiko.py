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
        pass

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
        else:
            print('Connect is failed!!!')

    except Exception as e:
        print(e)






































