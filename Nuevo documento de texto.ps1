cd notebooks
$clave = 1234
"storageaccount=$clave"|Set-Content keys.txt
"storageaccountkey"|Add-Content keys.txt

git pull
git add .
git commit -m "Mensaje automatizado"
git push