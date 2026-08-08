from __future__ import annotations

import ctypes
import platform
from ctypes import wintypes
from typing import Protocol


class SecretStoreUnavailableError(RuntimeError):
    """Raised when a platform cannot safely persist Planner credentials."""


class CredentialManagerAdapter(Protocol):
    def write(self, target: str, secret: str) -> None: ...

    def read(self, target: str) -> str | None: ...

    def delete(self, target: str) -> None: ...


class _NativeCredential(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", ctypes.c_byte * 8),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]


class WindowsCredentialManager:
    """Small ctypes adapter for Windows Credential Manager generic credentials."""

    _TYPE_GENERIC = 1
    _PERSIST_LOCAL_MACHINE = 2
    _NOT_FOUND = 1168

    def __init__(self) -> None:
        if platform.system() != "Windows":
            raise SecretStoreUnavailableError("Windows Credential Manager is unavailable on this platform")
        self._advapi32 = ctypes.WinDLL("Advapi32.dll", use_last_error=True)
        self._advapi32.CredWriteW.argtypes = [ctypes.POINTER(_NativeCredential), wintypes.DWORD]
        self._advapi32.CredWriteW.restype = wintypes.BOOL
        self._advapi32.CredReadW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(_NativeCredential))]
        self._advapi32.CredReadW.restype = wintypes.BOOL
        self._advapi32.CredDeleteW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
        self._advapi32.CredDeleteW.restype = wintypes.BOOL
        self._advapi32.CredFree.argtypes = [ctypes.c_void_p]
        self._advapi32.CredFree.restype = None

    def write(self, target: str, secret: str) -> None:
        blob = secret.encode("utf-16-le")
        buffer = (ctypes.c_ubyte * len(blob)).from_buffer_copy(blob)
        credential = _NativeCredential(
            Type=self._TYPE_GENERIC,
            TargetName=target,
            CredentialBlobSize=len(blob),
            CredentialBlob=ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)),
            Persist=self._PERSIST_LOCAL_MACHINE,
            UserName="SafeCodeHarness",
        )
        if not self._advapi32.CredWriteW(ctypes.byref(credential), 0):
            raise OSError(ctypes.get_last_error(), "Credential Manager write failed")

    def read(self, target: str) -> str | None:
        result = ctypes.POINTER(_NativeCredential)()
        if not self._advapi32.CredReadW(target, self._TYPE_GENERIC, 0, ctypes.byref(result)):
            error = ctypes.get_last_error()
            if error == self._NOT_FOUND:
                return None
            raise OSError(error, "Credential Manager read failed")
        try:
            credential = result.contents
            raw = ctypes.string_at(credential.CredentialBlob, credential.CredentialBlobSize)
            return raw.decode("utf-16-le")
        finally:
            self._advapi32.CredFree(result)

    def delete(self, target: str) -> None:
        if not self._advapi32.CredDeleteW(target, self._TYPE_GENERIC, 0):
            error = ctypes.get_last_error()
            if error != self._NOT_FOUND:
                raise OSError(error, "Credential Manager delete failed")


class SecretStore:
    """Persist the Planner key only through an OS credential manager adapter."""

    _TARGET = "SafeCodeHarness/PlannerApiKey"

    def __init__(
        self,
        adapter: CredentialManagerAdapter | None = None,
        platform_name: str | None = None,
    ) -> None:
        self._platform_name = platform_name or platform.system()
        self._adapter = adapter

    def set(self, secret: str) -> None:
        self._require_adapter().write(self._TARGET, secret)

    def get(self) -> str | None:
        return self._require_adapter().read(self._TARGET)

    def clear(self) -> None:
        self._require_adapter().delete(self._TARGET)

    def _require_adapter(self) -> CredentialManagerAdapter:
        if self._platform_name != "Windows":
            raise SecretStoreUnavailableError("Windows Credential Manager is required; no plaintext fallback is available")
        if self._adapter is None:
            try:
                self._adapter = WindowsCredentialManager()
            except (OSError, SecretStoreUnavailableError) as exc:
                raise SecretStoreUnavailableError("Windows Credential Manager is unavailable") from exc
        return _FailClosedCredentialManager(self._adapter)


class _FailClosedCredentialManager:
    """Convert adapter failures to a safe, secret-free public exception."""

    def __init__(self, adapter: CredentialManagerAdapter) -> None:
        self._adapter = adapter

    def write(self, target: str, secret: str) -> None:
        try:
            self._adapter.write(target, secret)
        except Exception as exc:
            raise SecretStoreUnavailableError("Windows Credential Manager operation failed") from exc

    def read(self, target: str) -> str | None:
        try:
            return self._adapter.read(target)
        except Exception as exc:
            raise SecretStoreUnavailableError("Windows Credential Manager operation failed") from exc

    def delete(self, target: str) -> None:
        try:
            self._adapter.delete(target)
        except Exception as exc:
            raise SecretStoreUnavailableError("Windows Credential Manager operation failed") from exc
