"""Main module."""

# TODO: make wdm class

import logging
import subprocess
import os
import json
from subprocess import DEVNULL
from sys import stderr # TODO: check Python 3.3 above
from wdm import WebosDevice
from wdm.exceptions import DetachError

# TODO: set logging level
STDIN = DEVNULL  # quiet, None for info level

from wdm.check import detach_image, get_stderr, get_vboxmanage, is_safe_to_create, is_vm_exists, is_vm_running
from wdm.check import VBOXM

here = os.path.abspath(os.path.dirname(__file__))
VM_JSON = json.loads(open(os.path.join(here, "wdm.json"), encoding='utf-8').read())

def detach_storage(name):
    """detach the image from the vm

    Args:
        name (str): vm name
    """
    vmcmd = VBOXM
    command = [vmcmd] + ['storageattach', name, '--storagectl', name, '--type',
                         'hdd', '--medium', 'emptydrive', '--port', '0', '--device', '0']
    if subprocess.call(command, stdin=STDIN, stderr=get_stderr()) == 0:
        return True
    else:
        return False

def attach_storage(vmcmd, name, vmimage):
    """attach the image to the vm

    Args:
        vmcmd (str): virtualizer command
        name (str): vm name
    """
    command = [vmcmd] + ['storageattach', name, '--storagectl', name, '--type',
                         'hdd', '--port', '0', '--device', '0', '--medium', vmimage]
    if subprocess.call(command, stdin=STDIN, stderr=get_stderr()) == 0:
        return True
    else:
        return False

def remove_vm(name):
    """remove vm

    Args:
        name (str): vm name
    """
    if VBOXM == None:
        print("wdm : Please install virtualbox.")
        return False
    
    if is_vm_exists(name):
        detach_storage(name)
        command = [VBOXM] + ['unregistervm', name, '--delete']
        if subprocess.call(command, stdin=STDIN, stderr=get_stderr()) == 0:
            return True
        else:
            raise DetachError(vmname=name)
    return False

def create_vm(vm: WebosDevice):
    """create a vm
    
    Temporal method for create vm.
    wdm class will be made sooner.

    Args:
        vm (WebosDevice): vm object
    """
    name = vm.name
    if is_safe_to_create(name):
        logging.info("%s is safe to create." % name)
        try:
            remove_vm(name)
        except DetachError as e:
            logging.error("wdm error : %s" % e)
            return False
    
    # TODO: error handling
    try:
        logging.info("creating vm....")
        command = [VBOXM] + ['createvm', '--ostype', 'Linux_64', '--register', '--name', name]
        subprocess.check_call(command, stdin=STDIN)
        command = [VBOXM] + ['storagectl', name, '--add', 'ide', '--name', name]
        subprocess.check_call(command, stdin=STDIN)
        command = [VBOXM] + ['modifyvm', name, '--boot1', 'disk', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none']
        subprocess.check_call(command, stdin=STDIN)
        
        # setting memory, videoram and cpu
        command = [VBOXM] + ['modifyvm', name, '--memory', vm.ram, '--vram', vm.vram, '--ioapic', 'on', '--cpus', vm.cpus]
        subprocess.check_call(command, stdin=STDIN)
        
        # setting graphics stuffs
        command = [VBOXM] + ['modifyvm', name, '--graphicscontroller', 'vmsvga']
        subprocess.check_call(command, stdin=STDIN)
        command = [VBOXM] + ['modifyvm', name, '--accelerate3d', 'on']
        subprocess.check_call(command, stdin=STDIN)
        
        # set usb tablet and sound
        command = [VBOXM] + ['modifyvm', name, '--mouse', 'usbtablet', '--audio', 'pulse', '--audioout', 'on', '--audioin', 'on']
        subprocess.check_call(command, stdin=STDIN)
        
        # setting network
        command = [VBOXM] + ['modifyvm', name, '--nic1', 'nat', '--natpf1', 'ssh,tcp,,'+ vm.hostssh  +',,22']
        subprocess.check_call(command, stdin=STDIN)
        command = [VBOXM] + ['modifyvm', name, '--natpf1', 'web-inspector,tcp,,9998,,9998']
        subprocess.check_call(command, stdin=STDIN)
        command = [VBOXM] + ['modifyvm', name, '--natpf1', 'enact-browser-web-inspector,tcp,,9223,,9999']
        subprocess.check_call(command, stdin=STDIN)
        
        # serial to null
        command = [VBOXM] + ['modifyvm', name, '--uart1', '0x3f8', '4', '--uartmode1', 'file', '/dev/null']
        subprocess.check_call(command, stdin=STDIN)
        
        # two display
        command = [VBOXM] + ['modifyvm', name, '--monitorcount', '2']
        subprocess.check_call(command, stdin=STDIN)
        
        # scale factor to 0.7
        command = [VBOXM] + ['setextradata', name, 'GUI/ScaleFactor', '0.7']
        subprocess.check_call(command, stdin=STDIN)
    except subprocess.CalledProcessError as e:
        print("wdm : creation error")
        logging.debug("creation error : %s" % e)
    else: # creation success
        if vm.image: # TODO: just create a vm without an image?
            attach_storage(VBOXM, name, vm.image)
        
def start_vm(vm: WebosDevice):
    """start a vm

    Args:
        vm (WebosDevice): vm object
    """
    if is_vm_exists(vm.name):
        # TODO: use is_vm_running below
        if is_safe_to_create(vm.name): # TODO: check image is attached meaning for now, we must create a vm with -i option
            command = [VBOXM] + ['startvm', vm.name]
            if subprocess.call(command, stdin=STDIN , stderr=get_stderr()) != 0:
                print("wdm : start error")

def stop_vm(vm: WebosDevice):
    """stop a vm

    Args:
        vm (WebosDevice): vm object
    """
    if is_vm_exists(vm.name):
        if is_vm_running(vm.name):
            command = [VBOXM] + ['controlvm', vm.name, 'poweroff']
            if subprocess.call(command, stdin=STDIN, stderr=get_stderr()) != 0:
                logging.debug("power off vm goes wrong!")
                print("wdm : stop error")
        else:
            print("wdm : vm is not running.")

def delete_vm(vm: WebosDevice):
    """delete a vm

    Args:
        vm (WebosDevice): vm object
    """
    if is_vm_exists(vm.name):
        if not is_vm_running(vm.name):
            if detach_image(vm.name):
                command = [VBOXM] + ['unregistervm', vm.name, '--delete']
                if subprocess.call(command, stdin=STDIN, stderr=get_stderr()) != 0:
                    logging.error("wdm error : delete_vm failed")
                    logging.debug("reason : unregistervm failed ")
            else:
                print("wdm : delete_vm failed")
        else:
            print("wdm : vm is running. please stop vm before delete")