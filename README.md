# Metrics for SciWIn
The Metrics shown below have been calculated using the GitHub API for each of the 2 SciWIn projects tracked in this repository. Presentation is done via a CWL Workflow and the scripts in this repository.


## SciWIn-Client
![SciWIn-Client downloads](sciwin_badge.svg)

SciWIn-Client helps users creating **Computational Workflows** in CWL. Detailed information about SciWIn-Client can be found in the [GitHub Repository](https://github.com/fairagro/sciwin).

### Downloads by Version
SciWIn-Client currently has about 699 overall downloads across all versions and operating systems. The latest version v2.0.0-beta.3 currently has 0 downloads.


![downloads by version](sciwin_release.png)


| Version | Downloads |
|---------|-----------|
| v2.0.0-beta.3 | 0|
| v2.0.0-beta.2 | 0|
| v2.0.0-beta.1 | 2|
| v1.2.2 | 16|
| v1.2.1 | 15|
| v1.2.0 | 57|
| v1.1.0 | 59|
| v1.0.0 | 106|
| v0.8.0 | 49|
| v0.7.0 | 37|
| v0.6.1 | 36|
| v0.6.0 | 21|
| v0.5.2 | 44|
| v0.5.1 | 34|
| v0.5.0 | 33|
| v0.4.0 | 31|
| v0.3.0 | 52|
| v0.2.0 | 38|
| v0.1.0 | 69|


### Downloads by Operating System
There are 267 downloads of the Linux build, 187 downloads of the Windows build and 174 downloads of the macOS build.


![downloads by platform](sciwin_platform.png)


| Platform | Downloads |
|---------|-----------|
| MacOS (ARM64) | 94|
| Linux (ARM64) | 78|
| MacOS (x64) | 80|
| Windows (x64) | 187|
| Linux (x64) | 189|



## SciWIn-Studio
![SciWIn-Studio downloads](sciwin_studio_badge.svg)

SciWIn-Studio is the desktop application for SciWIn, available for Windows, macOS and Linux. Detailed information about SciWIn-Studio can be found in the [GitHub Repository](https://github.com/fairagro/sciwin_studio).

### Downloads by Version
SciWIn-Studio currently has about 10 overall downloads across all versions and operating systems. The latest version v1.0.0-beta.4 currently has 5 downloads.


![downloads by version](sciwin_studio_release.png)


| Version | Downloads |
|---------|-----------|
| v1.0.0-beta.4 | 5|
| v1.0.0-beta.3 | 2|
| v1.0.0-beta.1 | 3|


### Downloads by Operating System
There are 1 downloads of the Linux build, 5 downloads of the Windows build and 0 downloads of the macOS build.


![downloads by platform](sciwin_studio_platform.png)


| Platform | Downloads |
|---------|-----------|
| Windows (x64) | 5|
| MacOS (ARM64) | 0|
| Linux (x64) | 1|
| MacOS (x64) | 0|
| Linux (ARM64) | 0|



## Historical Download Chart
The historical download chart below shows how the 709 combined downloads across all tracked projects progressed over time, using the commited data of this repository.


![downloads by date](history.png)

## Creating this Workflow
This Metrics are collected by a CWL Workflow which was created using SciWIn-Client itself.

The first tool being used in the `collect` tool which was created by the following command. Note that `--no-commit` option, which is needed to not leak my GitHub Token. The token was manually replaced by an input variable.
```bash
s4n create -c Dockerfile -t metrics --env .env --enable-network --no-commit  python metrics/collect.py \> raw_data.json
```
The other tools are quite easy to create_
```bash
s4n create -c Dockerfile -t metrics python metrics/analyze.py --json raw_data.json \> analyzed_data.json 
s4n create -c Dockerfile -t metrics -i .git -i analyzed_data.json python metrics/provenance.py \> provenance_data.json
s4n create -c Dockerfile -t metrics python metrics/announce.py --json analyzed_data.json
```
 
The connections are created as follows:
```bash
s4n connect pipeline --from token --to collect/token
s4n connect pipeline --from git --to provenance/git

s4n connect pipeline --from collect/raw_data --to analyze/json
s4n connect pipeline --from analyze/analyzed_data --to announce/json
s4n connect pipeline --from analyze/analyzed_data --to provenance/analyzed_data_json     

s4n connect pipeline --from collect/raw_data --to raw_data 
s4n connect pipeline --from analyze/analyzed_data --to analyzed_data
s4n connect pipeline --from analyze/badge --to badge
s4n connect pipeline --from analyze/platform --to platform
s4n connect pipeline --from analyze/release --to release
s4n connect pipeline --from announce/README --to readme
s4n connect pipeline --from provenance/history --to history
```

```mermaid
---
config:
  theme: base
  look: neo
  themeVariables:
    primaryColor: '#C5E0B4'
    primaryTextColor: '#231f20'
    secondaryColor: '#EEEEEE'
    lineColor: '#385723'    
    fontSize: 12px
    tertiaryTextColor: '#231f20'
    fontFamily: 'Fira Sans, trebuchet ms, verdana, arial'
---
flowchart TB
  linkStyle default stroke:#385723,stroke-width: 2px;
  subgraph inputs[Workflow Inputs]
    direction TB
    token(token)
    git(git)
  end
  subgraph outputs[Workflow Outputs]
    direction TB
    raw_data(raw_data)
    analyzed_data(analyzed_data)
    badge(badge)
    platform(platform)
    readme(readme)
    release(release)
    history(history)
  end
    collect(collect)
  token --> |token|collect
    analyze(analyze)
  collect --> |json|analyze
    announce(announce)
  analyze --> |json|announce
    announce_templates_template_md(../../templates/template.md)
  announce_templates_template_md --> |templates_template_md|announce
    provenance(provenance)
  git --> |git|provenance
  analyze --> |analyzed_data_json|provenance
  collect --> |raw_data|raw_data
  analyze --> |analyzed_data|analyzed_data
  analyze --> |badge|badge
  analyze --> |platform|platform
  announce --> |readme|readme
  analyze --> |release|release
  provenance --> |history|history
  style inputs fill:#EEEEEE,stroke-width:2px;
  style token stroke:#0f9884,fill:#6FC1B5,stroke-width:2px;
  style git stroke:#0f9884,fill:#6FC1B5,stroke-width:2px;
  style outputs fill:#EEEEEE,stroke-width:2px;
  style raw_data stroke:#823909,fill:#F8CBAD,stroke-width:2px;
  style analyzed_data stroke:#823909,fill:#F8CBAD,stroke-width:2px;
  style badge stroke:#823909,fill:#F8CBAD,stroke-width:2px;
  style platform stroke:#823909,fill:#F8CBAD,stroke-width:2px;
  style readme stroke:#823909,fill:#F8CBAD,stroke-width:2px;
  style release stroke:#823909,fill:#F8CBAD,stroke-width:2px;
  style history stroke:#823909,fill:#F8CBAD,stroke-width:2px;
  style collect stroke:#385723,stroke-width:2px;
  style analyze stroke:#385723,stroke-width:2px;
  style announce stroke:#385723,stroke-width:2px;
  style announce_templates_template_md font-size:9px,fill:#cfeae6, stroke:#9FD6CE,stroke-width:2px;
  style provenance stroke:#385723,stroke-width:2px;
```