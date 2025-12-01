# Fix Windows PulseAudio Server
1. Download a working PulseAudio for Windows:

Get it from: https://github.com/pgaskin/pulseaudio-win32/releases

2. Run the installer with basic settings.

3. Add the following to your `.bashrc` file in WSL:
```
export HOST_IP=$(ipconfig.exe | grep "IPv4 Address" | awk '{print $NF}' | head -n 1)
export PULSE_SERVER=tcp:$HOST_IP
```

4. `source .bashrc`

5. Ask AI for help after none of this works...
