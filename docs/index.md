# run-dagger-py

`run-dagger-py` is a composite action to prepare the environment and run a Firestarter workflow, using the Dagger Python SDK.

## Getting started

### Pre-requisites

To use this action to run a Firestarter workflow, you need:

- A Poetry project with the dependency with firestarter-workflows configured, and an optional dependencies group defined, with the name of the firestarter workflow to launch.
  - This workflow can be one of the standard firestarter workflows (see firestarter-workflows), or a local workflow, defined as an python package under the `firestarter.workflow.<workflow_name>` name, that exports a `run(vars:dict=None, secrets:dict=None, config_file:str=None) -> Int` method:
  - `vars`: `dict()` extracted from the `input.vars` input of the action (using TOML format)
  - `secrets`: `dict()` extracted from the `input.secrets` input of the action (using TOML format)
  - `config_file`: string with the path to the config file (if any)

See the example for more details: [test-repo-rundagger](https://github.com/prefapp/test-repo-rundagger/blob/main/.dagger/pyproject.toml)

### Usage

For a GitHub workflow you can use this action passing the following inputs:

- `worflow`: **mandatory**. Name of the workflow to run, must match the name of the package (without the `firestarter.workflows.` prefix), for example: `pr_verify`
- `working_directory`: **optional**. Path of the directory, from the GITHUB_WORKSPACE, where this action will be executed. Default to `${{ github.workspace }}`
- `pyproject_path`: **optional**. Path of the pyproject.toml project. Default to `${{ inputs.working_directory}}/.dagger`
- `vars`: **optional**. Config variables to pass to the workflow, in [Key/Value TOML format](https://toml.io/en/v1.0.0#keyvalue-pair)
- `secrets`: **optional**. Secrets to pass to the workflow, in [Key/Value TOML format](https://toml.io/en/v1.0.0#keyvalue-pair)
- `config_file`: **optional**. Path of the related workflow config file inside the repository, if any, from the `${{ inputs.working_directory }}`
- `python_version`: **optional**. Python version to use. Default to `3.11`. **Needs to be >= 3.10**

#### Example

```yaml
  build-images:
    runs-on: ubuntu-22.04
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          ref: ${{ github.event.inputs.from }}
          path: build

      - name: Checkout repository to get config file
        uses: actions/checkout@v3
        with:
          path: config

      - name: Run build_images firestarter workflow
        uses: prefapp/run-dagger-py@main
        with:
          working_directory: build
          pyproject_path: .dagger
          workflow: build_images
          config_file: ../config/config.yaml
          vars: |
            repo_name="${{ github.repository }}"
            from_point="${{ github.event.inputs.from }}"
            on_premises="${{ github.event.inputs.on_premises }}"
          secrets: |
            github_token="${{ github.token }}"
```
