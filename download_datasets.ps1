$ErrorActionPreference = 'Stop'
$root = 'E:\Repos\repo'
$hf = @(
  @{Name='CORD'; Repo='naver-clova-ix/cord-v2'},
  @{Name='WildReceipt'; Repo='kaydee/wildreceipt'},
  @{Name='SROIE'; Repo='mychen76/ds_receipts_v2_train'},
  @{Name='NutriGreen'; Repo='Voxel51/NutriGreen'},
  @{Name='IDSpace'; Repo='cactuslab/IDSpace'},
  @{Name='CUAD'; Repo='theatticusproject/cuad'},
  @{Name='MAUD'; Repo='theatticusproject/maud'},
  @{Name='FUNSD'; Repo='nielsr/funsd'},
  @{Name='RVL-CDIP'; Repo='aharley/rvl_cdip'}
)
foreach ($x in $hf) {
  $dir = Join-Path $root $x.Name
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $api = "https://huggingface.co/api/datasets/$($x.Repo)"
  $metaPath = Join-Path $dir 'dataset_api.json'
  curl.exe -L --fail --retry 3 $api -o $metaPath
  $meta = Get-Content $metaPath -Raw | ConvertFrom-Json
  $readme = "https://huggingface.co/datasets/$($x.Repo)/resolve/main/README.md?download=true"
  try { curl.exe -L --fail --retry 3 $readme -o (Join-Path $dir 'README.md') } catch { }
  $license = Join-Path $dir 'SOURCE.txt'
  "source=https://huggingface.co/datasets/$($x.Repo)`nrepo=$($x.Repo)`nlicense=$($meta.cardData.license)`nretrieved=$(Get-Date -Format o)" | Set-Content -Encoding UTF8 $license
  foreach ($s in $meta.siblings) {
    $f = $s.rfilename
    if ($f -match '\.(parquet|zip|tar|tgz|jsonl|json|csv)$') {
      $target = Join-Path $dir ($f -replace '/', '\')
      New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
      $url = "https://huggingface.co/datasets/$($x.Repo)/resolve/main/$f?download=true"
      if (-not (Test-Path $target)) {
        Write-Host "Downloading $($x.Name)/$f"
        curl.exe -L --fail --retry 3 $url -o $target
      }
    }
  }
}
