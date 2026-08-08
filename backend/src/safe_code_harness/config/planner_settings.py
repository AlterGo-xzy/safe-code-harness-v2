from dataclasses import dataclass


@dataclass(frozen=True)
class PlannerSettings:
    base_url: str
    model: str
    configured: bool
    masked_suffix: str | None

    @classmethod
    def from_secret(cls, base_url: str, model: str, secret: str | None) -> "PlannerSettings":
        return cls(
            base_url=base_url,
            model=model,
            configured=secret is not None,
            masked_suffix=secret[-4:] if secret else None,
        )
