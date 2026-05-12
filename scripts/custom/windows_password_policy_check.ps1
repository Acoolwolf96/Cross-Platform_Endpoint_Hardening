$passwordPolicy = net accounts
if ($passwordPolicy -match "Minimum password length.*8") { exit 0 } else { exit 1 }
