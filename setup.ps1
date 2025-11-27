# AI Assistant Setup Script for Windows
# This script helps you set up the AI Assistant project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI Assistant Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "  Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "✓ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose not found." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Environment Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
    $overwrite = Read-Host "Do you want to reconfigure? (y/N)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Skipping environment configuration..." -ForegroundColor Yellow
    } else {
        Remove-Item ".env"
        Copy-Item ".env.example" ".env"
        Write-Host "✓ Created new .env file" -ForegroundColor Green
    }
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file from template" -ForegroundColor Green
}

# Prompt for OpenAI API key
Write-Host ""
Write-Host "Please enter your OpenAI API Key:" -ForegroundColor Yellow
Write-Host "(Get one from: https://platform.openai.com/api-keys)" -ForegroundColor Gray
$apiKey = Read-Host "API Key"

if ($apiKey) {
    # Update .env file
    $envContent = Get-Content ".env"
    $envContent = $envContent -replace "OPENAI_API_KEY=.*", "OPENAI_API_KEY=$apiKey"
    $envContent | Set-Content ".env"
    Write-Host "✓ API key configured" -ForegroundColor Green
} else {
    Write-Host "⚠ No API key provided. You'll need to edit .env manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Building Docker Containers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$build = Read-Host "Do you want to build and start the containers now? (Y/n)"
if ($build -eq "n" -or $build -eq "N") {
    Write-Host ""
    Write-Host "Setup complete! To start the application later, run:" -ForegroundColor Green
    Write-Host "  docker-compose up --build" -ForegroundColor Cyan
    exit 0
}

Write-Host ""
Write-Host "Building containers... This may take 5-10 minutes on first run." -ForegroundColor Yellow
Write-Host ""

try {
    docker-compose up --build -d
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✓ All services are starting up..." -ForegroundColor Green
    Write-Host ""
    Write-Host "Access the application at:" -ForegroundColor Yellow
    Write-Host "  http://localhost" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "API Documentation:" -ForegroundColor Yellow
    Write-Host "  http://localhost/api/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To view logs:" -ForegroundColor Yellow
    Write-Host "  docker-compose logs -f" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To stop the application:" -ForegroundColor Yellow
    Write-Host "  docker-compose down" -ForegroundColor Cyan
    Write-Host ""
    
    # Wait a moment and check status
    Write-Host "Checking service status..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    docker-compose ps
    
} catch {
    Write-Host ""
    Write-Host "✗ Error building containers:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running manually:" -ForegroundColor Yellow
    Write-Host "  docker-compose up --build" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
Write-Host ""
