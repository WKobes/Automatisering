rm -rf ~/content
mkdir ~/content
cp ~/static/* ~/content/
mv ~/content/snapshot.html ~/content/index.html
if [ -d ./media ]; then
    mkdir -p ~/content/media/
    cp ./media/* ~/content/media/ 2>/dev/null || true
fi
