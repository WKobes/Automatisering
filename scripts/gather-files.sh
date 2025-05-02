rm -rf ~/content
mkdir ~/content
cp ~/static/* ~/content/
mv ~/content/snapshot.html ~/content/index.html
[ -d ./media ] && mkdir ~/content/media/
[ -d ./media ] && cp ./media/* ~/content/media/
