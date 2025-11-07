#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: metrics/provenance.py
    entry:
      $include: ../../metrics/provenance.py
  - entryname: .git
    entry: $(inputs.git)
  - entryname: analyzed_data.json
    entry: $(inputs.analyzed_data_json)
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: metrics

inputs:
- id: git
  type: Directory
  default:
    class: Directory
    location: ../../.git
- id: analyzed_data_json
  type: File
  default:
    class: File
    location: ../../analyzed_data.json

outputs:
- id: history
  type: File
  outputBinding:
    glob: history.png
- id: provenance_data
  type: File
  outputBinding:
    glob: provenance_data.json
stdout: provenance_data.json

baseCommand:
- python
- metrics/provenance.py
