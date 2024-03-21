{{- $profile := (vault (printf "kv/users/%s/mail" .profile)).data.data.profile -}}
{{- range $notmuch := (vault (printf "kv/users/%s/mail" .profile)).data.data.notmuch -}}

 #!/usr/bin/env python

from pathlib import Path
from os import path

MAILDIRS = [
{{- range $i, $maildirs := $notmuch.map.maildirs -}}
{{- if $i}}, {{ end -}}
{{ $maildirs | quote }}
{{- end }} ]

FOLDERS = [
{{- range $i, $folders := $notmuch.map.folders -}}
{{ if $i}},{{ end }}
    {{ $folders | quote }}
{{- end }}
{{-   end }}
]

with open(path.join (Path.home(), ".config/aerc/notmuchmap/{{ $profile }}.conf"), "w") as f:
    # RECENT
    s = "Recent=date:30days..today and not ("
    for i, m in enumerate(MAILDIRS):
        s += f"path:{m}/Spam/**"
        if i != len(MAILDIRS) - 1:
            s += " or "
    s += ")\n"
    f.write(s)

    # THREADED INBOX
    s = 'InboxThreaded=thread:"{'
    for i, m in enumerate(MAILDIRS):
        s += f"path:{m}/Inbox/**"
        if i != len(MAILDIRS) - 1:
            s += " or "
    s += '}"\n'
    f.write(s)

    # FOLDERS
    for folder in FOLDERS:
        s = f"{folder}="
        for i, m in enumerate(MAILDIRS):
            s += f"path:{m}/{folder}/**"
            if i != len(MAILDIRS) - 1:
                s += " or "
        if folder == "Archive":
            s += " or path:oldmail/**\n"
        else:
            s += "\n"
        f.write(s)
