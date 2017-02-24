param([string]$filename)
Write-Output $filename

$word = New-Object -ComObject word.application
$word.visible = $true
$fileIn = (Resolve-Path $filename).Path
$doc = $word.documents.open($fileIn)
$doc.SaveAs(($fileIn).replace("html","docx"), 16)
$doc.Close()
$word.Quit()