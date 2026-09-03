#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool
$namespaces:
  cwltool: http://commonwl.org/cwltool#

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: metrics/collect.py
    entry:
      $include: ../../metrics/collect.py
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: metrics
- class: NetworkAccess
  networkAccess: true
- class: EnvVarRequirement
  envDef:
    GITHUB_TOKEN: $(inputs.token)

inputs:
- id: token
  type: string
- id: repo
  type: string
  inputBinding:
    prefix: --repo

outputs:
- id: raw_data
  type: File
  outputBinding:
    glob: $(inputs.repo)_raw_data.json
stdout: $(inputs.repo)_raw_data.json

baseCommand:
- python
- metrics/collect.py

hints:
  cwltool:Secrets:
    secrets:
    - token
