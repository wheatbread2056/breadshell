# remove broken files from earlier installations
sudo rm -rf /usr/src/breadshell
sudo rm /bin/breadshell
# create the directory
sudo cp -r ./ /usr/src/breadshell/
# make launch.sh executable
sudo chmod +x /usr/src/breadshell/launch.sh
# make the link so breadshell can be used as a command
sudo ln /usr/src/breadshell/launch.sh /bin/breadshell
echo 'would you like to make breadshell the default shell? (Y/n)'
read choice
if [ '$choice' = 'Y' ]; then
    echo '/bin/breadshell' | sudo tee -a /etc/shells
    chsh -s /bin/breadshell
    echo breadshell is now the default shell, reboot to apply changes
else
    echo breadshell successfully installed
fi