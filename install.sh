echo "Checking dependencies"
echo ""

if ! hash python3
then
        echo "python3 could not be found"
        exit
else
        echo "python3 found"
fi

for MODULE in telegram.ext logging sys datetime pytz
do
        if python3 -c "import telegram.ext" &> /dev/null
        then
                echo "$MODULE found"
        else
                echo "$MODULE could not be found"
                exit
        fi
done
echo ""

echo "Editing the necessary files"
echo ""
sed -e "s/Bot Token/'$1'/g" -e "s/Chat ID/$2/g" -i ./InstanceElements.py
sed -e "s/\(Exec.*\) \/.*/\1 $(pwd | sed -e 's/\//\\\//g')\/Bot.py/g" ./Bot.service | sudo tee /lib/systemd/system/Bot.service > /dev/null

echo "Starting and enabling the service"
sudo systemctl start Bot.service
sudo systemctl enable Bot.service

