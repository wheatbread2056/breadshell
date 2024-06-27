echo 'are you running install.sh in the directory containing breadshell.py? the installation will not work if you do not do this (Y/n)'
read choice1
if [ "$choice1" = 'Y' ] || [ "$choice1" = 'y' ]; then
    echo proceeding with installation...
else
    exit
fi
# remove broken files from earlier installations
sudo rm -rf /usr/src/breadshell
sudo rm /bin/breadshell # legacy (pre 1.0)
sudo rm /sbin/breadshell
# create the directory
sudo cp -r ./ /usr/src/breadshell/
# make launch.sh executable
sudo chmod +x /usr/src/breadshell/launch.sh
# make the link so breadshell can be used as a command
sudo ln /usr/src/breadshell/launch.sh /sbin/breadshell
echo 'would you like to make breadshell the default shell? (Y/n)'
read choice
if [ "$choice" = 'Y' ]; then
    echo '/sbin/breadshell' > /dev/null | sudo tee -a /etc/shells
    chsh -s /sbin/breadshell
    echo breadshell is now the default shell, reboot to apply changes
else
    echo breadshell successfully installed
fi