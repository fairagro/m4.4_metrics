#!/usr/bin/env cwl-runner


cwlVersion: v1.2
class: Workflow

requirements:
- class: ScatterFeatureRequirement
- class: MultipleInputFeatureRequirement

inputs:
- id: token
  type: string
- id: git
  type: Directory
  default:
    class: Directory
    location: ../../.git
- id: repo
  type:
    type: array
    items: string

outputs:
- id: readme
  type: File
  outputSource: announce/README
- id: history
  type: File
  outputSource: provenance/history
- id: raw_data
  type:
    type: array
    items: File
  outputSource: collect/raw_data
- id: release
  type: File[]
  outputSource: analyze/release
- id: platform
  type: File[]
  outputSource: analyze/platform
- id: badge
  type: File[]
  outputSource: analyze/badge
- id: analyzed_data
  type: File[]
  outputSource: analyze/analyzed_data

steps:
- id: collect
  in:
  - id: token
    source: token
  - id: repo
    source: repo
  scatter: repo
  run: ../collect/collect.cwl
  out:
  - raw_data
- id: analyze
  in:
  - id: json
    source: collect/raw_data
  - id: name
    source: repo
  scatter:
  - name
  - json
  scatterMethod: dotproduct
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
  - id: name
    source: repo
  run: ../announce/announce.cwl
  out:
  - README
- id: provenance
  in:
  - id: git
    source: git
  - id: analyzed_data_json
    source: analyze/analyzed_data
  - id: name
    source: repo
  run: ../provenance/provenance.cwl
  out:
  - history
  - provenance_data
