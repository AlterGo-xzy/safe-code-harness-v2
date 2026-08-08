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
        executable = arguments[0].replace("\\", "/").rsplit("/", maxsplit=1)[-1]
        if not self.policy.blocks_command_executable(executable):
            return False

        recursive = False
        forced = False
        options_ended = False
        targets: list[str] = []
        for argument in arguments[1:]:
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

    @staticmethod
    def _is_root_target(target: str) -> bool:
        return target.startswith("/") and all(part in {"", ".", ".."} for part in target.split("/"))
