#!/bin/bash

git clone https://github.com/TheHappyAlien/Python_Game.git
cd ./Python_Game

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

pyinstaller ./Scripts/main.py --onefile --noconsole

mv ./SoundEffects ./dist
mv ./Sprites ./dist
mv ./high_score.txt ./dist/high_score.txt
rm -r ./Scripts
rm ./game_install.sh

cd ./dist

mv ./main ./PythonShooter
./PythonShooter
