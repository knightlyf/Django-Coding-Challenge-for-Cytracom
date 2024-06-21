#Variables
$tenantId = "e955ea3b-fb8d-447d-87b8-15fd44b1489b"
$appId = "bec08618-4b8b-4f05-bb28-8c4226b91ea9"
$password = "fb2832e1-0fb1-4800-a205-26d55e9764c9"
$vaultName = "AZ400Keys"
$secretName = "TestProj-automationps1-PAT"
$subscriptionId = "6238d801-162f-4858-a852-044d1fc92da4"
$organization = "Hydra-Industries"
$project = "TestProj"
$queryId = "e3195d68-5922-44e7-b486-1ff6d32e6580"

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $appId, $securePassword
Connect-AzAccount -ServicePrinicpal -Credential  $credential -Tenant $tenantId

Set-AzContext -SubscriptionId $subscriptionId

$secret = Get-AzKeyVaultSecret -VaultName $vaultName -Name $secretName

$PAT = $secret.SecretValueText
$releaseNotesPath = "$(System.DefaultWorkingDirectory)\releasenotes.md"

#Encode to base64 for HTTP header
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$($PAT)"))

#Azure calls
$queryUrl = "https://dev.azure.com/$organization/$project/_apis/wit/wiql/$queryId?api-version=6.0"
$response = Invoke-RestMethod - Uri $queryUrl -Method Get -Headers @{Authorization = ("Basic {0}" -f $base64AuthInfo) }

#Create markdown
$releaseNotes = @"
#release notes
This release contains the following updates:

"@

foreach ($workItem in $response.workItems) {

    $workItemUrl = $workItem.url
    $workItemDetails = Invoke-RestMethod -Uri $workItemUrl -Method Get Get -Headers @{Authorization = ("Basic {0}" -f $base64AuthInfo) }

    $releaseNotes += "## $($workItemDetails.fields.'System.Title')`n"
    $releaseNotes += "$($workItemDetails.fields.'System.Description')`n`n"
}

#Write to markdown
$releaseNotes | Out-File -FilePath $releaseNotesPath -Encoding utf8