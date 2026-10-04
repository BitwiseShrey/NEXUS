$word = New-Object -ComObject Word.Application
$word.Visible = $False
$docPath = "C:\Users\shrey\OneDrive\Desktop\NEXUS\NEXUS_Capstone_Phase_I_Report.docx"
$pdfPath = "C:\Users\shrey\OneDrive\Desktop\NEXUS\NEXUS_Capstone_Phase_I_Report.pdf"
try {
    $doc = $word.Documents.Open($docPath)
    $wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)
    $doc.Close()
    Write-Host "PDF Export Successful: $pdfPath"
} catch {
    Write-Error $_
} finally {
    $word.Quit()
}
