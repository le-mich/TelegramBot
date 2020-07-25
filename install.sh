if [[ ! -f ./bot.py || ! -f ./bot.service ]]
then
        echo "One or more files are missing or this is not the right base directory"
        echo "Exiting"
        exit
fi

echo "Checking dependencies:\n"

if ! hash python3
then
        echo "\tpython3 could not be found"
        echo "Exiting"
        exit
else
        echo "\tpython3 found"
fi

for MODULE in telegram.ext logging sys datetime
do
        if python3 -c "import $MODULE" &> /dev/null
        then
                echo "\t$MODULE found"
        else
                echo "\t$MODULE could not be found"
                echo "Exiting"
                exit
        fi
done

if [ ! -f ./instanceElements.py ]
then
        echo "\nCreating instanceElements.py"
        echo "TK = '$1'" > instanceElements.py
        echo "GID = $2" >> instanceElements.py
fi

echo "\nCreating and editing the service file"
sed -e "s/\(Exec.*\) \/.*/\1 $(pwd | sed -e 's/\//\\\//g')\/bot.py/g" ./bot.service | sudo tee /lib/systemd/system/bot.service > /dev/null

echo "\nStarting and enabling the service"
sudo systemctl start bot.service
sudo systemctl enable bot.service
