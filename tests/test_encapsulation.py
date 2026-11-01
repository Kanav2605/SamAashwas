import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_encapsulation_html_elements():
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Verify Workspace Mode Bar and Mode Selector
    assert "workspace-mode-bar" in html
    assert "workspace-mode-selector" in html
    assert "btn-mode-citizen" in html
    assert "btn-mode-admin" in html
    assert "data-role-access=\"citizen\"" in html
    assert "data-role-access=\"admin\"" in html

    # Verify Officer Admin Login Modal
    assert "admin-login-modal" in html
    assert "admin-preset-grid" in html
    assert "Er. Vikas Rao" in html
    assert "Chief Commissioner" in html
    assert "Er. Arvind Saxena" in html
    assert "admin-login-id" in html
    assert "admin-login-pass" in html
    assert "submitAdminLoginForm" in html

    # Verify Spotlight Command Palette
    assert "command-palette-modal" in html
    assert "cmd-palette-input" in html
    assert "openCommandPalette" in html

def test_admin_vs_citizen_role_access():
    # 1. Citizen login
    cit_res = client.post("/api/v1/auth/login", json={"preset_id": "rajesh_kumar"})
    assert cit_res.status_code == 200
    cit_token = cit_res.json()["access_token"]
    assert cit_res.json()["user"]["is_admin"] is False

    # 2. Admin login
    adm_res = client.post("/api/v1/auth/admin-login", json={"officer_id": "admin", "password": "admin123"})
    assert adm_res.status_code == 200
    adm_token = adm_res.json()["access_token"]
    assert adm_res.json()["user"]["is_admin"] is True

    # 3. Check me profiles reflect correct encapsulation
    cit_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {cit_token}"}).json()
    adm_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {adm_token}"}).json()

    assert cit_me["is_admin"] is False
    assert cit_me["role"] == "Citizen"

    assert adm_me["is_admin"] is True
    assert adm_me["role"] in ["Admin", "Municipal Administrator"]
