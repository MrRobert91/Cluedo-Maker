# Script para renombrar las fotos a formato: nombre_foto.extension

$fotosPath = "c:\Users\david\Desktop\Cluedo-Maker\backend\experiments\fotos"

# Mapeo de archivos originales a nuevos nombres
$renameMap = @{
    "01F9A9B6-B095-4EFC-A664-65E6DDF11803 - Sara García Pedrero.jpeg" = "sara_foto.jpeg"
    "20250722_193726 - Guillermo Sevillano.jpg" = "guillermo_foto.jpg"
    "83959c35-f40b-4eca-9587-c83e8a2c6051 - Jaime Vinuesa Alonso.jpeg" = "jaime_foto.jpeg"
    "Alejandro (Escri).jpeg" = "alejandro_foto.jpeg"
    "Ana Alonso - Ana Alonso.jpeg" = "ana_foto.jpeg"
    "e031c98c-5ff4-49db-9319-38d22be44c76 - Beatriz Blasco.jpeg" = "beatriz_foto.jpeg"
    "E7B13867-A7FA-4307-B40C-CF9C6CC6D90F - Victoria Rosado.jpeg" = "victoria_foto.jpeg"
    "f12585dd-738c-4b04-b830-dae9238de8d5 - Charo Alvarez Vazquez.jpeg" = "charo_foto.jpeg"
    "IMG_0061 - Rodrigo Gómez.jpeg" = "rodrigo_foto.jpeg"
    "IMG_0546 - Adriana Revelles Ros.jpeg" = "adriana_foto.jpeg"
    "IMG_1565 - Arturo Alonso Guerra.png" = "arturo_foto.png"
    "IMG_1666 - Elena Fernandez.jpeg" = "elena_foto.jpeg"
    "IMG_9522 - Aitor Martin.jpeg" = "aitor_foto.jpeg"
    "Isabel - Isabel Parrilla.jpg" = "isabel_foto.jpg"
    "Iñaki - iñaki martin.jpg" = "iñaki_foto.jpg"
    "Jose - Jose Garcia.jpg" = "jose_foto.jpg"
    "Lola - Lola García Bayón.png" = "lola_foto.png"
    "Lucía V - Lucia Valverde Gomez.jpg" = "lucía_foto.jpg"
    "Miguel_Tapiador_Foto - Miguel Tapiador.JPG" = "miguel_foto.jpg"
    "Monica - Monica Blazquez.jpg" = "mónica_foto.jpg"
    "NICO - Nico DN.jpg" = "nico_foto.jpg"
    "Sandra Herreras - Sandra Herreras Monteoliva.png" = "sandra_foto.png"
    "Silvia Martínez (Sil) - Silvia Martinez Ferreiro.jpg" = "sil_foto.jpg"
    "Stephania - Stephania Colorado.jpg" = "stephania_foto.jpg"
    "Susana en tamaño mediano - Susana Alvarez.png" = "susana_foto.png"
}

Write-Host "Renombrando archivos..." -ForegroundColor Cyan
Write-Host ""

$count = 0
foreach ($oldName in $renameMap.Keys) {
    $newName = $renameMap[$oldName]
    $oldPath = Join-Path $fotosPath $oldName
    $newPath = Join-Path $fotosPath $newName
    
    if (Test-Path $oldPath) {
        try {
            Rename-Item -Path $oldPath -NewName $newName -ErrorAction Stop
            Write-Host "✓ $oldName -> $newName" -ForegroundColor Green
            $count++
        }
        catch {
            Write-Host "✗ Error renombrando $oldName : $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "⚠ No se encontró: $oldName" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Proceso completado: $count archivos renombrados." -ForegroundColor Cyan
