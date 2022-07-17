import subprocess


MEDIA_DEVICE = None # Set this to your usb device, or `None` to use the media folder directly


def mount_media(func):
    def inner(*args, **kwargs):
         
        if MEDIA_DEVICE is not None:
            # Mount media device to media directory
            subprocess.run(["sudo", "mount", MEDIA_DEVICE, "media"], check=True)
         
        # getting the returned value
        returned_value = func(*args, **kwargs)
        
        if MEDIA_DEVICE is not None:
            # Unmount media device
            subprocess.run(["sudo", "umount", "media"], check=True)
         
        # returning the value to the original frame
        return returned_value
         
    return inner