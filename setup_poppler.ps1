# PowerShell script to download and setup Poppler
$downloadUrl = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0-0/Release-23.08.0-0.zip"
$outputZip = "poppler.zip"
$popplerDir = "poppler"

# Create poppler directory if it doesn't exist
New-Item -ItemType Directory -Force -Path $popplerDir

# Download Poppler
Write-Host "Downloading Poppler..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $outputZip

# Extract the zip file
Write-Host "Extracting Poppler..."
Expand-Archive -Path $outputZip -DestinationPath $popplerDir -Force

# Clean up zip file
Remove-Item $outputZip

Write-Host "Poppler has been downloaded and extracted to $popplerDir"
