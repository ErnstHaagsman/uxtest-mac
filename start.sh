# First do prerequisites

echo -n "Headphones plugged in? [y/N] "
read headphones

HP=`echo $headphones | tr '[:upper:]' '[:lower:]'`

if [ "$HP" != "y" ]; then
    echo "Could you please make sure they are plugged in, and then restart."
    exit 1
fi

while [ -z "$name" ]; do
    echo -n "What is the your name? "
    read name
done

echo $name > name.txt

echo "Alright, let's get started..."

echo "Please do NOT touch the keyboard or mouse until you see the countdown"

sleep 2

open ./start_camtasia.app

open -a Preview ~/Desktop/Instructions.pdf