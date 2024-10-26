from typing import NamedTuple

from github import Auth

from awx_plugin_credential_github import exceptions

CredentialPlugin = NamedTuple("CredentialPlugin", ["name", "inputs", "backend"])

github_app_inputs = {
    "fields": [
        {"id": "app_id", "label": "Application ID", "type": "string", "required": True},
        {"id": "installation_id", "label": "Installation ID", "type": "string", "required": True},
        {"id": "private_key", "label": "Private Key", "type": "string", "required": True, "secret": True},
        {"id": "jwt_expiry", "label": "JWT Token Expiry (sec)", "type": "integer", "default": 600},
    ]
}


def github_app_backend(**kwargs):
    app_id = kwargs.get("app_id")
    installation_id = kwargs.get("installation_id")
    private_key = kwargs.get("private_key")
    jwt_expiry = kwargs.get("jwt_expiry", 600)

    missing = []
    if not app_id:
        missing.append("Application ID")
    if not private_key:
        missing.append("Private Key")
    if missing:
        raise exceptions.MissingParameterError(missing)

    auth = Auth.AppAuth(app_id=app_id, private_key=private_key, jwt_expiry=jwt_expiry).get_installation_auth(
        installation_id=installation_id
    )

    return auth.token


github_app_plugin = CredentialPlugin(
    "GitHub App Authentication Plugin", inputs=github_app_inputs, backend=github_app_backend
)
