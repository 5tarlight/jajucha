if [[ $(uname -p) == 'arm' ]]; then
  arch -x86_64 /usr/local/bin/brew install python-tk
  arch -x86_64 /usr/local/bin/brew install pillow
else
  brew install python-tk
  brew install pillow
fi

pip3 uninstall opencv-python
pip3 uninstall opencv-contrib-python
pip3 uninstall opencv-contrib-python-headless

pip3 install -r requirements.txt