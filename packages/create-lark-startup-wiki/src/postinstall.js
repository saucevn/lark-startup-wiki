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
  console.log(`  ${c('pip install lark-startup-wiki')}  ${d('# or: pip install -r scripts/requirements.txt')}`);
  console.log('');
  console.log(b('Read these next:'));
  console.log(`  ${d('docs/lark-api-setup.md')}        ${d('# set up your Lark App')}`);
  console.log(`  ${d('skills/05-publish-workflow.md')} ${d('# publish discipline')}`);
  console.log('');
  console.log(b('Optional: install Claude Code plugin for live skill access:'));
  console.log(`  ${c('/plugin marketplace add saucevn/lark-startup-wiki')}`);
  console.log('');
}
