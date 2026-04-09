# Execution Adapter Pseudocode

```text
function dispatch_executor(command, envelope):
    adapter = load_adapter(command.executor.type)

    payload = {
        "correlation_id": envelope.envelope_id,
        "command_id": command.id,
        "actor": envelope.context.actor,
        "parameters": filter_allowed_parameters(
            envelope.parameters,
            command.allowed_parameters
        )
    }

    validate_payload(payload, command.input_schema_ref)

    if command.executor.type == "local_cli":
        return adapter.run_local_target(command.executor.target, payload)

    if command.executor.type == "github_action":
        return adapter.dispatch_workflow(command.executor.target, payload)

    if command.executor.type == "n8n_webhook":
        return adapter.post_webhook(command.executor.target, payload)

    if command.executor.type == "clawbot_tool":
        return adapter.invoke_tool(command.executor.target, payload)

    raise UnsupportedExecutor(command.executor.type)
```

Each adapter must return a normalized result that can be mapped into the
`CommandResult` or `FailureResult` contract before audit logging.
