#!/bin/bash
if [ ! -f "requirements.txt" ]; then
    touch requirements.txt
    pip freeze >> requirements.txt
    pip install --upgrade pip
    echo "Выгружен список библиотек окружения"
  else
    file="requirements.txt"
    pip install --upgrade pip
    for var in $(cat $file)
    do
        echo "Устанавливаю $var"
        pip install $var
    done
    echo "Все необходимые библиотеки установлены!"
fi