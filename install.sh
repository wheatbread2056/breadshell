# this is currently broken for some reason
sudo rm -rf /usr/src/breadshell
sudo cp -r ./ /usr/src/breadshell
sudo chmod +x /usr/src/breadshell/breadshell.py
sudo ln /usr/src/breadshell/breadshell.py /bin/breadshell
echo breadshell successfully installed