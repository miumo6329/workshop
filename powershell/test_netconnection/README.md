ネットワークの通信確認でpingをよく使用しますが、ポート番号指定での確認には、PowerShellのTest-NetConnectionを使うのが手軽です。

# 環境
* Windows 10 Home
* Windows PowerShell 5.1

# Test-NetConnectionについて
[公式ドキュメント](https://docs.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection?view=windowsserver2019-ps)

PowerShellを起動し下記コマンドを実行します。

```sh
> Test-NetConnection <ホスト名> -Port <ポート番号>
```
例えば、google.comのポート443番に対する結果。

```sh
> Test-NetConnection google.com -Port 443

ComputerName     : google.com
RemoteAddress    : 172.217.26.46
RemotePort       : 443
InterfaceAlias   : イーサネット
SourceAddress    : 192.168.11.2
TcpTestSucceeded : True
```

# 一括処理スクリプト

今回は、複数のホスト/ポート番号に対して一括で通信確認したかったので、CSVファイルに接続先情報をまとめて、一括処理する簡単なスクリプトを作成しました。

```powershell
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
```

上記のスクリプトと同階層のディレクトリに下記形式でCSVファイルを作成します。1列目を接続先ホスト、2列目をポート番号列として、2行目以降に追加していきます。

```csv
host,port
google.com,"80,443"
127.0.0.1,"80,3389,27017"
192.168.11.1,"80,443"
192.168.11.7,"25,110,80"
```

# セキュリティエラーが発生する場合

```sh
> .\test_netconnection.ps1
.\test_netconnection.ps1 : このシステムではスクリプトの実行が無効になっているため、ファイル F:\PowerShell\test_netconne
ction.ps1 を読み込むことができません。詳細については、「about_Execution_Policies」(https://go.microsoft.com/fwlink/?Lin
kID=135170) を参照してください。
発生場所 行:1 文字:1
+ .\test_netconnection.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : セキュリティ エラー: (: ) []、PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```
下記のコマンドでセキュリティポリシーを変更した上でスクリプト実行してください。実行中のプロセスのみポリシーを適用できます。

[公式ドキュメント](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7#parameters)

```sh
> Set-ExecutionPolicy RemoteSigned -Scope Process
> .\test_netconnection.ps1
```




