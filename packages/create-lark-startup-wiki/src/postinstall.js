// Print next-steps banner after scaffold.
import kleur from 'kleur';

export function printNextSteps({ targetDir, fileCount, initGit }) {
  const g = kleur.green;
  const c = kleur.cyan;
  const d = kleur.dim;
  const b = kleur.bold;

  console.log('');
  console.log(g(`✔ Created ${b(targetDir)}/  (${fileCount} files${initGit ? ', git initialized' : ''})`));
  console.log('');
  console.log(b('Next steps:'));
  console.log(`  ${c('cd ' + targetDir)}`);
  console.log(`  ${c('cp .env.example .env')}       ${d('# fill LARK_APP_ID, LARK_APP_SECRET')}`);
  console.log(`  ${c('pip install -r scripts/requirements.txt')}`);
  console.log(`  ${c('python scripts/validate_structure.py')}  ${d('# sanity check')}`);
  console.log('');
  console.log(b('Install the Claude Code plugin to load skills:'));
  console.log(`  ${c('/plugin marketplace add saucevn/lark-startup-wiki')}`);
  console.log(`  ${c('/plugin install lark-startup-wiki@saucevn')}`);
  console.log('');
  console.log(b('Reference docs (in the public lark-startup-wiki repo):'));
  console.log(`  ${d('https://github.com/saucevn/lark-startup-wiki/blob/main/docs/lark-api-setup.md')}`);
  console.log(`  ${d('https://github.com/saucevn/lark-startup-wiki/blob/main/skills/05-publish-workflow.md')}`);
  console.log('');
}
