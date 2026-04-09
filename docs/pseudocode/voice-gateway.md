# Voice Gateway Pseudocode

```text
function handle_voice_event(raw_event):
    envelope = normalize_voice_event(raw_event)
    assert envelope.mode in ["capture", "command", "combined"]

    if envelope.mode == "capture":
        target = resolve_capture_target(envelope.context, envelope.parameters)
        note = render_markdown_note(target, envelope)
        write_note(note)
        append_audit("succeeded", envelope, command_id="note.capture")
        return note

    if envelope.mode == "command":
        command = resolve_command(envelope.transcript)
        validate_against_registry(command, envelope.parameters)
        decision = evaluate_policy(command, envelope)
        if decision.requires_confirmation:
            confirmation = request_confirmation(envelope, command)
            if not confirmation.approved:
                append_audit("blocked", envelope, command.id)
                return blocked_result(command)
        result = dispatch_executor(command, envelope)
        append_audit(result.status, envelope, command.id)
        return result

    if envelope.mode == "combined":
        note = render_markdown_note(resolve_capture_target(...), envelope)
        write_note(note)
        command = resolve_command(envelope.transcript)
        decision = evaluate_policy(command, envelope)
        if decision.blocked:
            append_note_link(note, decision)
            append_audit("blocked", envelope, command.id)
            return combined_result(note, decision)
        result = dispatch_executor(command, envelope)
        append_note_link(note, result)
        append_audit(result.status, envelope, command.id)
        return combined_result(note, result)
```

The important invariant is that capture writes, command resolution, policy
evaluation, and audit emission are explicit and separately testable.
