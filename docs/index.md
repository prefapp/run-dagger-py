# run-dagger-py

This is a composite action to prepare the environment and run a Dagger workflow, using the Dagger Python SDK.

## Getting started

To be able to use this action to run a dagger workflow locally, you must:
- create a Poetry project
- add the `poetry-dagger-plugin` poetry plugin
```
poetry self add git+https://github.com/prefapp/run-dagger-py.git@main#subdirectory=poetry-dagger-plugin
```
- add the `poetry-dagger-plugin.workflows` section to your `pyproject.toml` file, with the name of your Dagger module and an alias to call it
```toml
[tool.poetry-dagger-plugin.workflows]
test = "test_example"
test2 = "my_second_workflow"
```

The module `run()` method will be invoked, passing the following arguments:
- `vars`: `dict()` extracted from the `input.vars` input of the action (using TOML format)
- `secrets`: `dict()` extracted from the `input.secrets` input of the action (using TOML format)
- `config_file`: string with the path to the config file (if any)

See the example for more details: [test-example](examples/test-example)
