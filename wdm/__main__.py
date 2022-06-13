"""
This module implements the developer interface for wdm.

:class:`WebosDevice <WebosDevice> class focuses on the developer interface. 
    
"""
from typing import Optional

import wdm
from wdm.check import is_device_running
class WebosDevice:
    """Core developer interface for wdm."""
    
    def __init__(
        self,
        name: str
    ):
        """Construct a :class:`WebosDevice <WebosDevice>`.
        
        :param str name:
            A webOS device name.
        """
        self._name = name
        self._cpus: Optional[int] = 2  # number of CPUs
        self._ram: Optional[int] = 4096  # vm RAM, MBs
        self._vram: Optional[int] = 128  # vm video RAM, MBs
        self._hostssh: Optional[int] = 6622 # host to device ssh port number
        
        @property
        def name(self):
            """Return webOS device name"""
            return self._name
        
        @property
        def cpus(self):
            """Return webOS device number of CPUs """
            return self._cpus
        
        @property
        def ram(self):
            """Return webOS device RAM size in MBs"""
            return self._ram
        
        @property
        def vram(self):
            """Return webOS device Video RAM size in MBs"""
            return self._vram
        
        @property
        def hostssh(self):
            """Return webOS device host to device ssh port number"""
            return self._hostssh
        
    def create(self):
        """Create a webOS device
            
        For now, webOS device is emulator.
        Default emulator device is webOS OSE emulator.
            
        """
        print("create")
        is_device_running(self._name)
        