![GitHub release](https://img.shields.io/github/release/bmunoz89/alfred-wf-bluetooth-manager?style=for-the-badge)
![GitHub Releases](https://img.shields.io/github/downloads/bmunoz89/alfred-wf-bluetooth-manager/latest/total?style=for-the-badge)
![GitHub All Releases](https://img.shields.io/github/downloads/bmunoz89/alfred-wf-bluetooth-manager/total?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/bmunoz89/alfred-wf-bluetooth-manager?style=for-the-badge)

# 🚨 Supports Alfred 4 🚨

> Workflows created or edited in any version of Alfred are fundamentally incompatible with earlier versions, even if no new features are used.

https://www.deanishe.net/alfred-workflow/guide/update.html#id3

I am using alfred 4, therefore I cannot make it compatible with alfred 3

# 💻 Installation 👾

Install brew https://brew.sh/

And then run this command on a terminal:
```bash
brew install blueutil
```

## Python 2 and macOS Monterrey

https://www.alfredapp.com/help/kb/python-2-monterey/

This is the recommended solution by Alfred and the solution implemented from release 3.0.0 and above, therefore I don't recommend to upgrade your workflow if you don't have macOS Monterrey.

```bash
export PATH="/opt/homebrew/bin:/usr/local/bin:${PATH}"
eval "$(brew shellenv)"
brew install pyenv
pyenv install 2.7.18
ln -s "${HOME}/.pyenv/versions/2.7.18/bin/python2.7" "${HOMEBREW_PREFIX}/bin/python"
```

Which should lead to have linked the python bin to this path `/usr/local/bin/python`.
To check if all the previous commands were successful, run this command:

```bash
/usr/local/bin/python --version
# Which should print this "Python 2.7.18"
```

## Download the release according to your OS version

macOS Monterey: [download][monterey last release link]
previous macOS: [download][last release link]

# 📸 Screenshots

![](./screenshots/ss_bset.jpg)
![](./screenshots/ss_bc.jpg)
![](./screenshots/ss_bcs.jpg)
![](./screenshots/ss_bds.jpg)
![](./screenshots/ss_bm.jpg)

# 🔑 Keywords

- `bset`: Set the default device
- `bc`: Connect the default device
- `bd`: Disconnect the default device
- `bcs`: Select the device you would like to connect to
- `bds`: Select the device you would like to disconnect to
- `bm`:
    - Bluetooth on and off
    - Enable and disabled check of updates
    - Manually check for an update
    - Clear data: Allowing to clear the blueutil path saved(just in case 🤷🏽‍♂️)

Default device = Is the device used in `bc` and `bd` commands without having to select one like in `bcs` or `bds`.

# 🆘 Help

## - What should I do if a get the message "Change your blueutil or brew path"?

![](./screenshots/command_error.jpg)

To get them, run the following commands in your own terminal:
```bash
> which brew # paste this command
/usr/local/bin/brew # this is just an example result
> which blueutil # and paste this one
/usr/local/bin/blueutil # this is just an example result
```

Copy both results and follow the steps in the next point.

---

## - How to set my own `brew`/`blueutil` path?

### Step 1: Open your Alfred settings inside the workflows panel

![](./screenshots/settings_1.jpg)

### Step 2: Press the button "Configure workflow and variables"

![](./screenshots/settings_2.jpg)

### Step 3: Edit `bluetooth_command_path` or `brew_command_path` variables with your own

![](./screenshots/settings_3.jpg)


Easy peasy! 😋

[monterey last release link]: https://github.com/bmunoz89/alfred-wf-bluetooth-manager/releases/latest/download/Bluetooth.manager.alfredworkflow
[last release link]: https://github.com/bmunoz89/alfred-wf-bluetooth-manager/releases/download/2.4.1/Bluetooth.manager.alfredworkflow