class WdmError(Exception):
    """Base wdm exception that others inherit.

    """
    
class VmError(WdmError):
    """VM related exception

    """
    
class DetachError(VmError):
    """vm detach error exception

    """
    def __init__(self, vmname:str):
        """Detach Error

        Args:
            vmname (str): vm name of exception occurred
        """
        super().__init__(f"[{vmname}] could not detach image")
        self.vnmame = vmname
