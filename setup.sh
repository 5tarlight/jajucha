if [[ $(uname -p) == 'arm' ]]; then
  ibrew install python-tk
  ibrew install pillow
else
  brew install python-tk
  brew install pillow
fi

pip3 uninstall opencv-python
pip3 uninstall opencv-contrib-python
pip3 uninstall opencv-contrib-python-headless

pip3 install -r requirements.txt