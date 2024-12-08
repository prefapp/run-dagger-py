# run-dagger-py
`run-dagger-py` is a composite action to prepare the environment and run a Firestarter workflow, using the Dagger Python SDK.

See [docs](docs/index.md) for more details.

## Inputs

- `workflow`: Name of the workflow to run, must match the name of the python package (without the `firestarter.workflows.` prefix), for example: `pr_verify`. **(required)**
- `config_file`: The firestarter config file path. Default is `.dagger/firestarter.yml`. **(required)**
- `python_version`: The Python version to use. Default is `3.11`. **Needs to be >= 3.10**. **(optional)**
- `working_directory`: The working directory to run the action in. Default is `${{ github.workspace }}`. **(optional)**
- `vars`: The var arguments to pass to the workflow (in [Key/Value TOML format](https://toml.io/en/v1.0.0#keyvalue-pair)). Default is `""`. **(optional)**
- `secrets`: The secrets to pass to the workflow (in [Key/Value TOML format](https://toml.io/en/v1.0.0#keyvalue-pair)). Default is `""`. **(optional)**
- `workflows_repository`: The repository from which to download workflows. Default is `prefapp/firestarter-workflows`. **(optional)**
- `workflows_repository_ref`: The workflows repository ref. Default is `main`. **(optional)**

## Usage

```yaml
name: Run Dagger Workflow
on: [push]

jobs:
  run-dagger:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        ref: ${{ github.event.inputs.from }}
        uses: actions/checkout@v4
      
      - name: Checkout repository to get config file
        uses: actions/checkout@v4
        with:
          path: config

      - name: Run Dagger Workflow
        uses: prefapp/run-dagger-py@main
        with:
          workflow: 'build-imagews'
          config_file: '../config/.github/build_images.yml'
          python_version: '3.11'
          working_directory: ${{ github.workspace }}
          vars: |
            YOUR_VARS_IN_TOML_FORMAT
          secrets: |
            YOUR_SECRETS_IN_TOML_FORMAT'
          workflows_repository: 'prefapp/firestarter-workflows'
          workflows_repository_ref: 'main'
```

## Steps

- Checkout tools repo: Uses actions/checkout@v4 to checkout the workflows repository.
- Install poetry: Installs Poetry version 1.8.3 using pipx.
- Setup Python: Uses actions/setup-python@v5 to setup Python with the specified version and cache.
- Install dependencies: Installs the dependencies using Poetry.
- Run Dagger workflow: Runs the specified Dagger workflow using the provided inputs.


## License

This project is licensed under the MIT License.