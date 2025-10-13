<#
SYNOPSIS
  Move mouse to (x,y) and perform click/double/right, or type text.

USAGE
  .\Invoke-Mouse.ps1 -x 500 -y 300 -operation click
  .\Invoke-Mouse.ps1 -x 500 -y 300 -operation double -delay 80
  .\Invoke-Mouse.ps1 -x 900 -y 600 -operation right
  .\Invoke-Mouse.ps1 -operation type -text "hello world"
  .\Invoke-Mouse.ps1 -x 700 -y 400 -operation type -text "admin@hp" -clickBeforeType
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [int]$x,

    [Parameter(Mandatory=$false)]
    [int]$y,

    [Parameter(Mandatory=$true)]
    [ValidateSet('click','double','right','type')]
    [string]$operation,

    # For -operation type
    [Parameter(Mandatory=123$false)]
    [string]$text,

    # Milliseconds: wait after move, and double-click interval
    [int]$delay = 100,

    # In type mode: click (x,y) first to focus
    [switch]$clickBeforeType
)

Add-Type -AssemblyName System.Windows.Forms | Out-Null

Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class MouseNative {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll")]
    public static extern void mouse_event(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);

    public const int MOUSEEVENTF_LEFTDOWN  = 0x02;
    public const int MOUSEEVENTF_LEFTUP    = 0x04;
    public const int MOUSEEVENTF_RIGHTDOWN = 0x08;
    public const int MOUSEEVENTF_RIGHTUP   = 0x10;
}
"@ | Out-Null

function Set-Cursor {
    param([int]$X, [int]$Y)
    if (-not [MouseNative]::SetCursorPos($X, $Y)) {
        throw "SetCursorPos failed for ($X,$Y)."
    }
}

function Invoke-LeftClick {
    [MouseNative]::mouse_event([MouseNative]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    [MouseNative]::mouse_event([MouseNative]::MOUSEEVENTF_LEFTUP,   0, 0, 0, 0)
}

function Invoke-RightClick {
    [MouseNative]::mouse_event([MouseNative]::MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    [MouseNative]::mouse_event([MouseNative]::MOUSEEVENTF_RIGHTUP,   0, 0, 0, 0)
}

# Parameter checks (ASCII-only messages to avoid encoding issues)
switch ($operation) {
    'click' {
        if (-not ($PSBoundParameters.ContainsKey('x') -and $PSBoundParameters.ContainsKey('y'))) {
            throw "click requires -x and -y."
        }
    }
    'double' {
        if (-not ($PSBoundParameters.ContainsKey('x') -and $PSBoundParameters.ContainsKey('y'))) {
            throw "double requires -x and -y."
        }
    }
    'right' {
        if (-not ($PSBoundParameters.ContainsKey('x') -and $PSBoundParameters.ContainsKey('y'))) {
            throw "right requires -x and -y."
        }
    }
    'type' {
        if (-not $PSBoundParameters.ContainsKey('text')) {
            throw "type requires -text ""your string""."
        }
        if ($clickBeforeType.IsPresent -and -not ($PSBoundParameters.ContainsKey('x') -and $PSBoundParameters.ContainsKey('y'))) {
            throw "type + -clickBeforeType requires -x and -y to focus first."
        }
    }
    default {
        throw "Unsupported operation: $operation"
    }
}

# Main
switch ($operation) {
    'click' {
        Set-Cursor -X $x -Y $y
        Start-Sleep -Milliseconds $delay
        Invoke-LeftClick
    }
    'double' {
        Set-Cursor -X $x -Y $y
        Start-Sleep -Milliseconds $delay
        Invoke-LeftClick
        Start-Sleep -Milliseconds $delay
        Invoke-LeftClick
    }
    'right' {
        Set-Cursor -X $x -Y $y
        Start-Sleep -Milliseconds $delay
        Invoke-RightClick
    }
    'type' {
        if ($clickBeforeType) {
            Set-Cursor -X $x -Y $y
            Start-Sleep -Milliseconds $delay
            Invoke-LeftClick
            Start-Sleep -Milliseconds $delay
        }
        # Note: SendKeys needs the target window focused.
        # Special characters need SendKeys escaping rules.
        [System.Windows.Forms.SendKeys]::SendWait($text)
    }
}
