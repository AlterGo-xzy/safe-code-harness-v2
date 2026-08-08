from dataclasses import dataclass
import shlex

from safe_code_harness.governance.policy import RuntimePolicy


@dataclass(frozen=True)
class GuardDecision:
    blocked: bool
    reason: str | None = None


class CommandGuard:
    """Deterministically block destructive shell commands without executing them."""

    def __init__(self, policy: RuntimePolicy) -> None:
        self.policy = policy

    def check(self, command: str) -> GuardDecision:
        arguments = self._parse(command)
        if arguments is None or self._contains_shell_syntax(arguments):
            return GuardDecision(blocked=True, reason="blocked command")
        if self._is_recursive_forced_root_deletion(arguments):
            return GuardDecision(blocked=True, reason="blocked command")
        return GuardDecision(blocked=False)

    def _parse(self, command: object) -> list[str] | None:
        if not isinstance(command, str) or not command.strip():
            return None
        try:
            lexer = shlex.shlex(command, posix=True, punctuation_chars="|&;<>()")
            lexer.commenters = ""
            lexer.whitespace_split = True
            arguments = list(lexer)
        except ValueError:
            return None
        return arguments or None

    @staticmethod
    def _contains_shell_syntax(arguments: list[str]) -> bool:
        return any(argument in {";", "&&", "||", "|", "&", "<", ">", "(", ")"} for argument in arguments)

    def _is_recursive_forced_root_deletion(self, arguments: list[str]) -> bool:
        unwrapped_arguments = self._unwrap_supported_wrappers(arguments)
        if unwrapped_arguments is None:
            return True

        executable = self._executable_name(unwrapped_arguments[0])
        if not self.policy.blocks_command_executable(executable):
            return False

        recursive = False
        forced = False
        options_ended = False
        targets: list[str] = []
        for argument in unwrapped_arguments[1:]:
            normalized_argument = argument.casefold()
            if not options_ended and argument == "--":
                options_ended = True
            elif not options_ended and normalized_argument == "--recursive":
                recursive = True
            elif not options_ended and normalized_argument == "--force":
                forced = True
            elif not options_ended and argument.startswith("-") and argument != "-":
                recursive = recursive or "r" in normalized_argument[1:]
                forced = forced or "f" in normalized_argument[1:]
            else:
                targets.append(argument)

        return recursive and forced and any(self._is_root_target(target) for target in targets)

    def _unwrap_supported_wrappers(self, arguments: list[str]) -> list[str] | None:
        current_arguments = arguments
        while True:
            executable = self._executable_name(current_arguments[0]).casefold()
            if executable == "env":
                current_arguments = self._unwrap_env(current_arguments[1:])
            elif executable == "sudo":
                current_arguments = self._unwrap_sudo(current_arguments[1:])
            elif executable == "command":
                current_arguments = self._unwrap_command(current_arguments[1:])
            else:
                return current_arguments
            if current_arguments is None:
                return None

    @staticmethod
    def _unwrap_env(arguments: list[str]) -> list[str] | None:
        index = 0
        while index < len(arguments):
            argument = arguments[index]
            if argument == "--":
                index += 1
                while index < len(arguments) and CommandGuard._is_env_assignment(arguments[index]):
                    index += 1
                return arguments[index:] or None
            if argument in {"-", "-i", "--ignore-environment"}:
                index += 1
            elif argument in {"-u", "--unset"}:
                if index + 1 >= len(arguments):
                    return None
                index += 2
            elif argument.startswith("--unset="):
                if not argument.removeprefix("--unset="):
                    return None
                index += 1
            elif argument.startswith("-"):
                return None
            elif CommandGuard._is_env_assignment(argument):
                index += 1
            else:
                return arguments[index:]
        return None

    @staticmethod
    def _unwrap_sudo(arguments: list[str]) -> list[str] | None:
        index = 0
        no_value_options = {"-n", "-E", "--non-interactive", "--preserve-env"}
        value_options = {"-u", "-g", "-h", "-C", "--user", "--group", "--host", "--close-from"}
        while index < len(arguments):
            argument = arguments[index]
            if argument == "--":
                return arguments[index + 1 :] or None
            if argument in no_value_options:
                index += 1
            elif argument in value_options:
                if index + 1 >= len(arguments):
                    return None
                index += 2
            elif argument.startswith("--user=") or argument.startswith("--group="):
                if not argument.partition("=")[2]:
                    return None
                index += 1
            elif argument.startswith("-"):
                return None
            else:
                return arguments[index:]
        return None

    @staticmethod
    def _unwrap_command(arguments: list[str]) -> list[str] | None:
        index = 0
        while index < len(arguments):
            argument = arguments[index]
            if argument == "--":
                return arguments[index + 1 :] or None
            if argument == "-p":
                index += 1
            elif argument.startswith("-"):
                return None
            else:
                return arguments[index:]
        return None

    @staticmethod
    def _executable_name(executable: str) -> str:
        return executable.replace("\\", "/").rsplit("/", maxsplit=1)[-1]

    @staticmethod
    def _is_env_assignment(argument: str) -> bool:
        name, separator, _ = argument.partition("=")
        return bool(separator) and bool(name) and (name[0].isalpha() or name[0] == "_") and all(
            character.isalnum() or character == "_" for character in name
        )

    @staticmethod
    def _is_root_target(target: str) -> bool:
        return target.startswith("/") and all(part in {"", ".", ".."} for part in target.split("/"))
