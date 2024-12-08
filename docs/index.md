# Pre-requisites

To use this action to run a Firestarter workflow, you need:

- A Poetry project with the dependency with firestarter-workflows configured, and an optional dependencies group defined, with the name of the firestarter workflow to launch.
  - This workflow can be one of the standard firestarter workflows (see firestarter-workflows), or a local workflow, defined as an python package under the `firestarter.workflow.<workflow_name>` name, that exports a `run(vars:dict=None, secrets:dict=None, config_file:str=None) -> Int` method:
  - `vars`: `dict()` extracted from the `input.vars` input of the action (using TOML format)
  - `secrets`: `dict()` extracted from the `input.secrets` input of the action (using TOML format)
  - `config_file`: string with the path to the config file (if any)

See the example for more details: [test-repo-rundagger](https://github.com/prefapp/test-repo-rundagger/blob/main/.dagger/pyproject.toml)
