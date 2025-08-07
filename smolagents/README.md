
python3 -m venv .venv
source .venv/bin/activate


sudo apt install direnv
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

echo "source .venv/bin/activate" > .envrc
direnv allow

# NOTES
# unset PS1 from the .envrc because of bash issues
# add the show env into ~/.bashrc to make sure venv is shown


