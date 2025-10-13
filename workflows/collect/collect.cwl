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

outputs:
- id: raw_data
  type: File
  outputBinding:
    glob: raw_data.json
stdout: raw_data.json

baseCommand:
- python
- metrics/collect.py

hints:
  cwltool:Secrets:
    secrets:
    - token
