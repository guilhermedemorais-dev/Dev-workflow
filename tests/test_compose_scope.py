"""Execute the scope CLI against synthetic Compose data, without Docker/network."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'plugins/devops-standard/skills/devops-standard/scripts/compose-scope.py'


class ComposeScope(unittest.TestCase):
    def setUp(self):
        self.base = {
            'name': 'fixture',
            'services': {'api': {'image': 'api:1'}, 'db': {'image': 'db:1'}},
            'volumes': {'data': {}}, 'networks': {'private': {}},
            'secrets': {'password': {'external': True}},
            'configs': {'settings': {'external': True}},
        }

    def run_guard(self, after, *allowed, before=None, raw=False):
        with tempfile.TemporaryDirectory() as folder:
            old, new = Path(folder) / 'old.json', Path(folder) / 'new.json'
            old.write_text(json.dumps(self.base if before is None else before))
            new.write_text(after if raw else json.dumps(after))
            result = subprocess.run([sys.executable, str(SCRIPT), '--before', str(old),
                                     '--after', str(new), *allowed], capture_output=True, text=True)
            self.assertEqual(result.stderr, '')
            output = json.loads(result.stdout)
            self.assertFalse(output['operationally_verified'])
            return result.returncode, output

    def test_noop_requires_no_permission(self):
        code, result = self.run_guard(self.base)
        self.assertEqual((code, result['status'], result['changes']), (0, 'WITHIN_SCOPE', []))

    def test_allowed_api_change_does_not_authorize_database(self):
        after = copy.deepcopy(self.base)
        after['services']['api']['image'] = 'api:2'
        self.assertEqual(self.run_guard(after, '--allow-services', 'api')[0], 0)
        after['services']['db']['image'] = 'db:2'
        code, result = self.run_guard(after, '--allow-services', 'api')
        self.assertEqual(code, 1)
        self.assertEqual([x['name'] for x in result['changes'] if not x['allowed']], ['db'])

    def test_redis_addition_and_database_removal_fail_closed(self):
        for action in ('add', 'remove'):
            with self.subTest(action=action):
                after = copy.deepcopy(self.base)
                if action == 'add':
                    after['services']['redis'] = {'image': 'redis:7'}
                else:
                    del after['services']['db']
                self.assertEqual(self.run_guard(after, '--allow-services', 'api')[0], 1)

    def test_every_resource_group_needs_its_own_permission(self):
        for kind, name in [('volumes', 'data'), ('networks', 'private'),
                           ('secrets', 'password'), ('configs', 'settings')]:
            with self.subTest(kind=kind):
                after = copy.deepcopy(self.base)
                after[kind][name] = {'name': 'replacement'}
                self.assertEqual(self.run_guard(after, '--allow-services', 'api')[0], 1)
                self.assertEqual(self.run_guard(after, '--allow-' + kind, name)[0], 0)

    def test_project_name_and_unknown_top_level_fields_are_protected(self):
        for field in ('name', 'x-custom'):
            with self.subTest(field=field):
                after = copy.deepcopy(self.base)
                after[field] = 'new'
                self.assertEqual(self.run_guard(after)[0], 1)
                self.assertEqual(self.run_guard(after, '--allow-fields', field)[0], 0)

    def test_literal_allow_list_does_not_interpret_globs(self):
        after = copy.deepcopy(self.base)
        after['services']['api']['image'] = 'api:2'
        self.assertEqual(self.run_guard(after, '--allow-services', '*')[0], 1)

    def test_invalid_and_duplicate_input_is_rejected_without_config_output(self):
        for raw in ('[]', '{"services": []}', '{"services":{"api":null}}',
                    '{"services":{"api":{}} ,"services":{}}',
                    '{"services":{"api": "sensitive-password"}}', 'sensitive-password'):
            with self.subTest(raw=raw):
                code, result = self.run_guard(raw, raw=True)
                self.assertEqual((code, result['status']), (2, 'INVALID_INPUT'))
                self.assertNotIn('sensitive-password', json.dumps(result))

    def test_missing_file_is_invalid(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--before', '/missing-before-59',
                                 '--after', '/missing-after-59'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['status'], 'INVALID_INPUT')

    def test_report_excludes_interpolated_values(self):
        after = copy.deepcopy(self.base)
        after['services']['api']['environment'] = {'PASSWORD': 'secret-synthetic-value'}
        code, result = self.run_guard(after, '--allow-services', 'api')
        self.assertEqual(code, 0)
        self.assertNotIn('secret-synthetic-value', json.dumps(result))
        self.assertNotIn('environment', json.dumps(result))

    def test_boolean_number_type_changes_outside_scope_are_rejected(self):
        for old, new in ((True, 1), (1, True), (False, 0), (0, False)):
            with self.subTest(old=old, new=new):
                before = copy.deepcopy(self.base)
                before['x-policy'] = {'nested': [old]}
                after = copy.deepcopy(before)
                after['services']['api']['image'] = 'api:2'
                after['x-policy']['nested'] = [new]
                self.assertEqual(self.run_guard(after, '--allow-services', 'api',
                                               before=before)[0], 1)

    def test_nonfinite_numbers_are_invalid_even_in_allowed_or_unchanged_data(self):
        for value in (float('nan'), float('inf'), float('-inf')):
            with self.subTest(value=value):
                after = copy.deepcopy(self.base)
                after['services']['api']['x-value'] = value
                self.assertEqual(self.run_guard(after, '--allow-services', 'api')[0], 2)
                self.assertEqual(self.run_guard(after, '--allow-services', 'api',
                                               before=after)[0], 2)

    def test_empty_resource_group_presence_is_a_scoped_top_level_change(self):
        before = {'services': {'api': {'image': 'api:1'}}}
        after = copy.deepcopy(before)
        after['networks'] = {}
        self.assertEqual(self.run_guard(after, '--allow-services', 'api', before=before)[0], 1)
        self.assertEqual(self.run_guard(after, '--allow-fields', 'networks', before=before)[0], 0)


if __name__ == '__main__':
    unittest.main()
