param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("up", "down", "left", "right", "win", "enter", "esc")]
    [string]$Key
)

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Keyboard {
    [DllImport("user32.dll", SetLastError=true)]
    public static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);
}
"@

# 虛擬鍵碼 (Virtual-Key Codes)
$vkCodes = @{
    "up"    = 0x26
    "down"  = 0x28
    "left"  = 0x25
    "right" = 0x27
    "win"   = 0x5B
    "enter" = 0x0D
    "esc"   = 0x1B
}

if (-not $vkCodes.ContainsKey($Key)) {
    Write-Host "Invalid key: $Key"
    exit 1
}

$vk = $vkCodes[$Key]

# 按下鍵
[Keyboard]::keybd_event($vk, 0, 0, 0)
Start-Sleep -Milliseconds 100
# 放開鍵
[Keyboard]::keybd_event($vk, 0, 2, 0)

Write-Host "Pressed key: $Key"
