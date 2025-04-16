{{/* Return the appropriate apiVersion for Horizontal Pod Autoscaler */}}
{{- define "apiVersion.hpa" }}
{{- if .Capabilities.APIVersions.Has "autoscaling/v2" }}
{{- print "autoscaling/v2" }}
{{- else if .Capabilities.APIVersions.Has "autoscaling/v2beta2"}}
{{- print "autoscaling/v2beta2" }}
{{- else }}
{{- print "autoscaling/v2beta1" }}
{{- end }}
{{- end }}

{{/* Return the appropriate apiVersion for ingress */}}
{{- define "apiVersion.ingress" }}
{{- if .Capabilities.APIVersions.Has "networking.k8s.io/v1" }}
{{- print "networking.k8s.io/v1" }}
{{- else if .Capabilities.APIVersions.Has "networking.k8s.io/v1beta1" }}
{{- print "networking.k8s.io/v1beta1" }}
{{- else }}
{{- print "extensions/v1beta1" }}
{{- end }}
{{- end }}

{{/* Return the appropriate apiVersion for deployment */}}
{{- define "apiVersion.deployment" }}
{{- if .Capabilities.APIVersions.Has "apps/v1" }}
{{- print "apps/v1" }}
{{- else }}
{{- print "extensions/v1beta1" }}
{{- end }}
{{- end }}
