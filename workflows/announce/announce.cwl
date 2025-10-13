#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: metrics/announce.py
    entry:
      $include: ../../metrics/announce.py
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: metrics

inputs:
- id: json
  type: File
  default:
    class: File
    location: ../../analyzed_data.json
  inputBinding:
    prefix: --json

outputs:
- id: README
  type: File
  outputBinding:
    glob: README.md

baseCommand:
- python
- metrics/announce.py
