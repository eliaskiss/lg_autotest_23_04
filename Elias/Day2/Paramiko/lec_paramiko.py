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
        pass

    ##############################################################
    # Check Connection
    ##############################################################
    def isAlive(self):
        pass

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







































