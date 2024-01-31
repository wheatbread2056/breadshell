# remove broken files from earlier installations
sudo rm -rf /usr/src/breadshell
sudo rm /bin/breadshell
# create the directory
sudo cp -r ./ /usr/src/breadshell/
# make launch.sh executable
sudo chmod +x /usr/src/breadshell/launch.sh
# make the link so breadshell can be used as a command
sudo ln /usr/src/breadshell/launch.sh /bin/breadshell
echo breadshell successfully installed