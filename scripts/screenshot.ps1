
function Save-Screenshot() {

    try {
        Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Drawing;
public class DPI {
    [DllImport("gdi32.dll")]
    static extern int GetDeviceCaps(IntPtr hdc, int nIndex);
    public enum DeviceCap {
    VERTRES = 10,
    DESKTOPVERTRES = 117
    }
    public static float scaling() {
    Graphics g = Graphics.FromHwnd(IntPtr.Zero);
    IntPtr desktop = g.GetHdc();
    int LogicalScreenHeight = GetDeviceCaps(desktop, (int)DeviceCap.VERTRES);
    int PhysicalScreenHeight = GetDeviceCaps(desktop, (int)DeviceCap.DESKTOPVERTRES);
    return (float)PhysicalScreenHeight / (float)LogicalScreenHeight;
    }
}
'@ -ReferencedAssemblies 'System.Drawing.dll' -ErrorAction Stop
        $scale = [DPI]::scaling()
    }
    catch {
        Write-Host "Failed to get DPI scaling"
        $Error[0]
        $scale = 1
    }
    
    Add-Type -AssemblyName System.Windows.Forms
    $screenBounds = [System.Windows.Forms.SystemInformation]::VirtualScreen

    $width = [int]($screenBounds.Width * $scale)
    $height = [int]($screenBounds.Height * $scale)
    $bitmap = New-Object System.Drawing.Bitmap($width, $height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    Add-Type -AssemblyName System.Drawing
    $leftTop = New-Object System.Drawing.Point
    $leftTop.X = [int]($screenBounds.Left * $scale)
    $leftTop.Y = [int]($screenBounds.Top * $scale)
    $size = New-Object System.Drawing.Point
    $size.X = $width
    $size.Y = $height
    $graphics.CopyFromScreen($leftTop, [System.Drawing.Point]::Empty, $size)

    $file_name_time = (Get-Date).toString("yyyy_MMdd_HH_mm_ss")
    $file_name = "screenshot_$file_name_time.png"
    $bitmap.Save($file_name, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
    return (get-item $file_name).FullName
}



Save-Screenshot