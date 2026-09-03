#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: metrics/analyze.py
    entry:
      $include: ../../metrics/analyze.py
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: metrics

inputs:
- id: json
  type: File
  default:
    class: File
    location: ../../raw_data.json
  inputBinding:
    prefix: --json
- id: name
  type: string
  inputBinding:
    prefix: --name

outputs:
- id: analyzed_data
  type: File
  outputBinding:
    glob: $(inputs.name)_analyzed_data.json
- id: badge
  type: File
  outputBinding:
    glob: $(inputs.name)_badge.svg
- id: platform
  type: File
  outputBinding:
    glob: $(inputs.name)_platform.png
- id: release
  type: File
  outputBinding:
    glob: $(inputs.name)_release.png
stdout: $(inputs.name)_analyzed_data.json

baseCommand:
- python
- metrics/analyze.py
