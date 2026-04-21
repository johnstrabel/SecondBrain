Set-Location "C:\Users\johnn\Brain"

git add -A

$changes = git status --porcelain
if ($changes) {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "vault backup $date"
    git push origin main
}
