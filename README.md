# Telegram Bot template

Based on [telegram.ext](https://python-telegram-bot.org/).

To keep the bot Token and the Chat ID secret I store them in `InstanceElements.py`, respectively as `TK` and `GID`.

Since this is supposed to run automatically on some kind of server (a RPi 3B+ in my case), I wrote a systemd service file.
To be placed in `/lib/systemd/system/`.

Refer to [systemd](https://wiki.archlinux.org/index.php/systemd) for more on the topic.

The provided `install.sh` is to be run inside the install folder with Token and Chat ID as arguments:
``` bash
./install.sh YourToken YourChatID
```
The script will check the dependencies, edit the `InstanceElements.py` file, edit the systemd service file with the correct path and place it in `/lib/systemd/system/`
(done using `sudo` as it needs write privileges), start and enable the Bot.service.

