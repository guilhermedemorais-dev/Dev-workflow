"""Structural starter checks only, not browser or future-agent behavior proof."""

from html.parser import HTMLParser
from pathlib import Path
import json
import re
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'plugins/ui-ux-standard/skills/ui-ux-standard'


class CatalogueParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class LiveDesignGuideTests(unittest.TestCase):
    def setUp(self):
        self.source = (SKILL / 'assets/live-design-guide/index.html').read_text()
        self.parser = CatalogueParser()
        self.parser.feed(self.source)

    def test_component_identity_and_local_navigation_resolve(self):
        elements = self.parser.elements
        ids = [attrs['id'] for _, attrs in elements if 'id' in attrs]
        self.assertEqual(len(ids), len(set(ids)))
        components = [attrs for _, attrs in elements if 'data-component-id' in attrs]
        self.assertTrue(components)
        for attrs in components:
            self.assertIn('id', attrs)
            self.assertTrue(attrs.get('data-revision'))
        for _, attrs in elements:
            for key in ('for', 'aria-controls'):
                if key in attrs:
                    self.assertIn(attrs[key], ids)
            if attrs.get('href', '').startswith('#'):
                self.assertIn(attrs['href'][1:], ids)

    def test_starter_is_self_contained_and_has_no_external_submissions(self):
        for tag, attrs in self.parser.elements:
            self.assertNotIn(tag, {'form', 'iframe'})
            self.assertNotIn('src', attrs)
            if 'href' in attrs:
                self.assertNotIn('://', attrs['href'])
        self.assertNotIn('fetch(', self.source)
        self.assertNotIn('XMLHttpRequest', self.source)

    def test_control_is_labelled_and_updates_a_status_region(self):
        elements = self.parser.elements
        labels = {attrs.get('for') for tag, attrs in elements if tag == 'label'}
        controls = [attrs for tag, attrs in elements if tag == 'select']
        self.assertTrue(controls)
        for control in controls:
            self.assertIn(control.get('id'), labels)
        self.assertTrue(any(attrs.get('role') == 'status' and
                            attrs.get('aria-live') == 'polite'
                            for _, attrs in elements))
        states = {attrs['value'] for tag, attrs in elements if tag == 'option'}
        self.assertEqual(states, {'default', 'loading', 'empty', 'error', 'success'})

    def test_instruction_reference_and_starter_are_shipped_together(self):
        self.assertTrue((SKILL / 'references/live-design-guide.md').is_file())
        self.assertTrue((SKILL / 'assets/live-design-guide/index.html').is_file())

    @unittest.skipUnless(shutil.which('node'), 'Node is needed for the isolated script smoke test')
    def test_fixture_script_transitions_without_network_capability(self):
        # Minimal DOM harness: executes JS, does not pretend to render a browser.
        script = re.search(r'<script>(.*?)</script>', self.source, re.S).group(1)
        states = [attrs['value'] for tag, attrs in self.parser.elements if tag == 'option']
        harness = r'''
const vm = require('node:vm');
const assert = require('node:assert/strict');
const payload = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
let listener;
const result = {textContent: ''};
const selector = {addEventListener: (event, callback) => {
  assert.equal(event, 'change'); listener = callback;
}};
const document = {getElementById: id => {
  if (id === 'fixture-state') return selector;
  if (id === 'fixture-result') return result;
  throw new Error('Unknown DOM target: ' + id);
}};
vm.runInNewContext(payload.script, {document}, {timeout: 1000});
assert.equal(typeof listener, 'function');
const messages = payload.states.map(value => {
  listener({target: {value}});
  assert.equal(typeof result.textContent, 'string');
  assert.ok(result.textContent.length > 0);
  return result.textContent;
});
assert.equal(new Set(messages).size, payload.states.length);
'''
        result = subprocess.run(
            [shutil.which('node'), '-e', harness],
            input=json.dumps({'script': script, 'states': states}),
            text=True, capture_output=True, timeout=5, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
