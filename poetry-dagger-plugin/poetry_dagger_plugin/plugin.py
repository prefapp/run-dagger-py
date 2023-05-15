import importlib
import os
import sys
import tomllib

from cleo.helpers import argument, option
from poetry.console.commands.group_command import GroupCommand
from poetry.plugins.application_plugin import ApplicationPlugin

from typing import Any, List


class RunDaggerWorkflow(GroupCommand):

    name = "run_dagger"
    description = "Execute a predefined dagger workflow from your pyproject.toml."

    arguments = [
        argument(
          "workflow",
          description="The dagger workflow to run from your pyproject.toml.",
          multiple=False
        ),
    ]

    options = [
        option(
            "config_file", None,
            description="Path to the config file.",
            value_required=False,
            multiple=False,
            flag=False,
        ),
        option(
            "vars", None,
            description="Vars to pass to the workflow.",
            multiple=False,
            value_required=False,
            default="",
            flag=False,
        ),
        option(
            "secrets", None,
            description="Secrets to pass to the workflow.",
            multiple=False,
            value_required=False,
            default="",
            flag=False,
        ),
    ]

    def handle(self) -> int:
        pyproject_folder_path = self.poetry.pyproject._file.path.parent
        pyproject_data = self.poetry.pyproject.data

        cmd_name = self.argument("workflow")
        cmd = (
            pyproject_data.get("tool", {})
            .get("poetry-dagger-plugin", {})
            .get("workflows", {})
            .get(cmd_name)
        )

        if not cmd:
            self.line_error(
                f"\nUnable to find the workflow '{cmd_name}'. To configure a command you must "
                "add it to your pyproject.toml under the path "
                "[tool.poetry-dagger-plugin.workflows]. For example:"
                "\n\n"
                "[tool.poetry-dagger-plugin.workflows]\n"
                f'test = "test_workflow"\n',
                style="error",
            )
            return 1


        # Change directory to the folder that contains the pyproject.toml so that the command runs
        # from that folder (even if you call poetry exec from a subfolder). This mimics the
        # behaviour of npm/yarn.
        os.chdir(pyproject_folder_path)
        workflow_module = f'{cmd}'
        print(f"Importing module {workflow_module} from {pyproject_folder_path}")

        # see https://docs.python.org/3/library/sys.html#sys.path
        sys.path.insert(0, str(pyproject_folder_path))
        workflow = importlib.import_module(workflow_module)

        self.line(f"Running workflow : {cmd}\n", style="info")

        result = workflow.run(
            vars=tomllib.loads(self.option("vars")),
            secrets=tomllib.loads(self.option("secrets")),
            config_file=self.option("config_file")
        )
        self.line(f"Result : {result}\n", style="info")
        self.line("\n✨ Done!")
        return 0


def factory() -> RunDaggerWorkflow:
    return RunDaggerWorkflow()


class ExecPlugin(ApplicationPlugin):
    def activate(self, application) -> None:
        application.command_loader.register_factory("run_dagger", factory)
