#! /bin/sh

if [ ! -f "./bot.py" ] || [ ! -f "./bot.service" ] || [ ! -f "./api.py" ]
then
        echo "One or more files are missing or this is not the right base directory"
        echo "Exiting"
        exit
fi

echo "=> Checking dependencies:"

if hash python3
then
        echo "\tpython3 found"
else
        echo "\tpython3 could not be found... "
        echo "Exiting"
        exit
fi

for MODULE in telegram.ext logging sys datetime
do
        if python3 -c "import $MODULE" 2> /dev/null
        then
                echo "\t$MODULE found"
        else
                echo "\t$MODULE could not be found... "
                echo "Exiting"
                exit
        fi
done

if [ ! -f ./instanceElements.py ]
then
        echo "=> Creating instanceElements.py"
        echo "TK = '$1'\nGID = '$2'" > instanceElements.py
else
		echo "=> instanceElements.py alredy present"
fi

if [ $( ps -p 1 -o comm= ) = "systemd" ]
then
		echo "=> Creating and editing the service file"
		sed "s/\(Exec.*\) \/.*/\1 $(pwd | sed 's/\//\\\//g')\/bot.py/g" ./bot.service | sudo tee /lib/systemd/system/bot.service > /dev/null

		echo "=> Starting and enabling the service"
		sudo systemctl start bot.service
		sudo systemctl enable bot.service
else
		echo "=> Systemd not present, skipping..."
fi

echo "Done :)"
