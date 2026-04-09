# Voice Gateway

This runtime will accept normalized transcript payloads, classify voice mode,
and pass typed requests to the router. It is intentionally separate from the
knowledge and policy definitions so those remain repo-native.

Combined-mode coordination is implemented in `apps.voice_gateway.combined_mode`
and writes notes before invoking the governed command path.
