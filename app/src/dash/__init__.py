from dash import dash

import os
import sys
import redis
import time
import subprocess
import json
import argparse

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)



def runme(command):
  commandlist = command.split(" ")
  result = subprocess.run(commandlist, capture_output=True)
  payload = {"returncode": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr }
  return payload


def main():
    parser = argparse.ArgumentParser(description="Keep dash and automate", usage="dash <action> \n\n \
               \
               version : 1.0.0\n\
               actions:\n\
               stutus        Run dash from systemd service \n  \
               service        Run dash from systemd service \n  \
               initservice    setup dash systemd service \n  \
               stopservice    disable and cleanup dash systemd service \n  \
               startservice   setup and enable dash systemd service \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = True


    if args.action[0] == "service":
        print("dash run as if was a systemd service")
        dash.dash()
        
        

    if ready and args.action[0] == "initservice":
        runme("sudo touch /etc/dash/dash.service.token")
        runme("sudo touch /etc/systemd/system/dash.service")
        runme("sudo chown knowit:knowit /etc/dash/dash.service.token")
        runme("sudo chown knowit:knowit /etc/systemd/system/dash.service")
        myservice = open("/etc/systemd/system/dash.service", "w")
        myservice.write("[Unit]\n")
        myservice.write("Description=Ansible Automation on Ansible Automation\n")
        myservice.write("After=network.target\n")
        myservice.write("[Service]\n")
        myservice.write("ExecStart=/usr/local/bin/dash service\n")
        myservice.write("User=dash\n")
        myservice.write("Restart=always\n")
        myservice.write("[Install]\n")
        myservice.write("WantedBy=default.target\n")
        myservice.write("RequiredBy=network.target\n")
        myservice.close
        runme("sudo systemctl daemon-reload")
        ready  = False

    if ready and ( args.action[0] == "reset" or args.action[0] == "stopservice"):
        runme("sudo systemctl daemon-reload")
        runme("sudo systemctl disable dash.service")
        runme("sudo systemctl stop dash.service")
        ready  = False

    if ready and ( args.action[0] == "reset" or args.action[0] == "startservice"):
        runme("sudo systemctl daemon-reload")
        runme("sudo systemctl enable dash.service")
        runme("sudo systemctl start dash.service")
        ready  = False


    





