#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: metrics/announce.py
    entry:
      $include: ../../metrics/announce.py
  - entryname: templates/template.md
    entry: $(inputs.templates_template_md)
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
- id: templates_template_md
  type: File
  default:
    class: File
    location: ../../templates/template.md

outputs:
- id: README
  type: File
  outputBinding:
    glob: README.md

baseCommand:
- python
- metrics/announce.py
