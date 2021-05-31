$path = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $path
$csv = Import-Csv "address.csv" -Encoding ASCII
Start-Transcript "result.txt"
foreach($row in $csv){
    $host_ip = $row.host
    foreach($port in $row.port.Split(",")){
        Test-NetConnection $host_ip -Port $port
    }
}
Stop-Transcript