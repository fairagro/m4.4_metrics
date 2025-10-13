#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

inputs:
- id: token
  type: string

outputs:
- id: raw_data
  type: File
  outputSource: collect/raw_data
- id: analyzed_data
  type: File
  outputSource: analyze/analyzed_data
- id: badge
  type: File
  outputSource: analyze/badge
- id: platform
  type: File
  outputSource: analyze/platform
- id: readme
  type: File
  outputSource: announce/README
- id: release
  type: File
  outputSource: analyze/release

steps:
- id: collect
  in:
  - id: token
    source: token
  run: ../collect/collect.cwl
  out:
  - raw_data
- id: analyze
  in:
  - id: json
    source: collect/raw_data
  run: ../analyze/analyze.cwl
  out:
  - analyzed_data
  - badge
  - platform
  - release
- id: announce
  in:
  - id: json
    source: analyze/analyzed_data
  run: ../announce/announce.cwl
  out:
  - README
