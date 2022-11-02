$clave = 1234
$clave2 = 12345
"storageaccountname"|Set-Content keys.txt
$clave|Add-Content keys.txt

"storageaccoun2"|Add-Content keys.txt
$clave2|Add-Content keys.txt

git pull
git add .
git commit -m "Mensaje automatizado"
git push