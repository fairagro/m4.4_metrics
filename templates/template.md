# Metrics for SciWIn
The Metrics shown below have been calculated using the GitHub API for each of the {{software|length}} SciWIn projects tracked in this repository. Presentation is done via a CWL Workflow and the scripts in this repository.

{% for sw in software %}
## {{sw.title}}
![{{sw.title}} downloads]({{sw.name}}_badge.svg)

{% if sw.description %}{{sw.description}} {% endif %}Detailed information about {{sw.title}} can be found in the [GitHub Repository]({{sw.url}}).

### Downloads by Version
{{sw.title}} currently has about {{sw.downloads}} overall downloads across all versions and operating systems. The latest version {{sw.latest_version}} currently has {{sw.latest_downloads}} downloads.


![downloads by version]({{sw.name}}_release.png)


| Version | Downloads |
|---------|-----------|
{% for key, value in sw.versions.items() %}| {{key}} | {{value}}|
{% endfor %}

### Downloads by Operating System
There are {{sw.os.get('Linux', 0)}} downloads of the Linux build, {{sw.os.get('Windows', 0)}} downloads of the Windows build and {{sw.os.get('MacOS', 0)}} downloads of the macOS build.


![downloads by platform]({{sw.name}}_platform.png)


| Platform | Downloads |
|---------|-----------|
{% for key, value in sw.platform.items() %}| {{key}} | {{value}}|
{% endfor %}

{% endfor %}
## Historical Download Chart
The historical download chart below shows how the {{total_downloads}} combined downloads across all tracked projects progressed over time, using the commited data of this repository.


![downloads by date](history.png)
