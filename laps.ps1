$username = $arg[0]
$password = $arg[1]

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword

$ProcessInfo = New-Object System.Diagnostics.ProcessStartInfo

#With FileName we're basically telling powershell to run another powershell process
$ProcessInfo.FileName = "powershell.exe"

#CreateNoWindow helps avoiding a second window to appear whilst the process runs
$ProcessInfo.CreateNoWindow = $true

#Note the line below contains the Working Directory where the script will start from
$ProcessInfo.WorkingDirectory = $env:windir
$ProcessInfo.RedirectStandardError = $true 
$ProcessInfo.RedirectStandardOutput = $true 
$ProcessInfo.UseShellExecute = $false

#The line below is basically the command you want to run and it's passed as text, as an argument
$ProcessInfo.Arguments = "Get-AdmPwdPassword -Computername $($args[2])"

#The next 3 lines are the credential for UserB, as you can see, we can't just pass $Credential
$ProcessInfo.Username = $Credential.GetNetworkCredential().username
$ProcessInfo.Domain = $Credential.GetNetworkCredential().Domain
$ProcessInfo.Password = $Credential.Password

#Finally start the process and wait for it to finish
$Process = New-Object System.Diagnostics.Process 
$Process.StartInfo = $ProcessInfo 
$Process.Start() | Out-Null 
$Process.WaitForExit() 

#Grab the output
$GetProcessResult = $Process.StandardOutput.ReadToEnd()

#Print the Job results
$GetProcessResult