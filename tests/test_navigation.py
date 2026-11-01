import re
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_all_views_and_navigation_targets_exist():
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Extract all view container IDs
    view_containers = set(re.findall(r'<div[^>]+id="([^"]+)"[^>]+class="[^"]*view-container', html))
    view_containers.update(re.findall(r'<div[^>]+class="[^"]*view-container[^"]*"[^>]+id="([^"]+)"', html))

    expected_views = {
        'home-view',
        'citizen-portal',
        'field-tasks-view',
        'triage-view',
        'dispatch-view',
        'transparency-view',
        'command-center',
        'gallery-view',
        'rewards-view',
        'predictive-view',
        'jan-sunwai-view',
        'agent-view',
        'whatsapp-simulator'
    }

    assert expected_views.issubset(view_containers), f"Missing views: {expected_views - view_containers}"

    # Extract all tab-btn targets
    tab_targets = set(re.findall(r'class="[^"]*tab-btn[^"]*"[^>]+data-tab="([^"]+)"', html))
    tab_targets.update(re.findall(r'data-tab="([^"]+)"[^>]+class="[^"]*tab-btn', html))

    for tab in tab_targets:
        assert tab in view_containers, f"Tab button data-tab='{tab}' does not match any view-container!"

    # Verify all switchTab calls in HTML target real views
    switch_calls = set(re.findall(r'switchTab\(\'([^\']+)\'\)', html))
    for sc in switch_calls:
        assert sc in view_containers, f"switchTab('{sc}') does not match any view-container!"

def test_hash_routing_map():
    with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    m = re.search(r'const hashMap = \{([^}]+)\};', app_js)
    assert m is not None, "hashMap definition not found in app.js"

    hash_lines = m.group(1).strip().split('\n')
    routes = {}
    for hl in hash_lines:
        hl = hl.strip().strip(',')
        if hl:
            parts = hl.split(':')
            v_id = parts[0].strip().strip("'\"")
            route = parts[1].strip().strip("'\"")
            routes[v_id] = route

    assert len(routes) == 13
    assert routes['home-view'] == '#/'
    assert routes['citizen-portal'] == '#/report'
    assert routes['field-tasks-view'] == '#/field'
    assert routes['triage-view'] == '#/officer/triage'
    assert routes['dispatch-view'] == '#/officer/dispatch'
    assert routes['transparency-view'] == '#/transparency'
    assert routes['command-center'] == '#/map'
    assert routes['gallery-view'] == '#/gallery'
    assert routes['rewards-view'] == '#/rewards'
    assert routes['predictive-view'] == '#/risk'
    assert routes['jan-sunwai-view'] == '#/jan-sunwai'
    assert routes['agent-view'] == '#/agents'
    assert routes['whatsapp-simulator'] == '#/whatsapp'
