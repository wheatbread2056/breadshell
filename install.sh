# this is currently broken for some reason
sudo rm -rf /usr/src/bsh
sudo cp -r ./ /usr/src/bsh
sudo chmod +x /usr/src/bsh/breadshell.py
sudo ln /usr/src/bsh/breadshell.py /bin/breadshell
echo breadshell successfully installed