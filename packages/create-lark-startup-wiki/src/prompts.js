// Interactive prompts via @clack/prompts
import { intro, text, confirm, outro, isCancel, cancel } from '@clack/prompts';
import kleur from 'kleur';

// Extract space_id from URL like:
// https://acme.larksuite.com/wiki/space/7123456789
// https://acme.larksuite.com/wiki/Yix7wqkiXi2ksNkqHyylk6C1gqh
export function parseWikiSpaceId(url) {
  if (!url) return '';
  const m = url.match(/\/wiki\/(?:space\/)?([A-Za-z0-9]+)/);
  return m ? m[1] : url.trim();
}

// Extract base app_token from URL like:
// https://acme.larksuite.com/base/Bas123456abc
export function parseBaseAppToken(url) {
  if (!url) return '';
  const m = url.match(/\/base\/([A-Za-z0-9]+)/);
  return m ? m[1] : url.trim();
}

// Extract tenant from a Lark URL: https://<tenant>.larksuite.com/...
export function parseTenant(url) {
  if (!url) return '';
  const m = url.match(/https?:\/\/([^.]+)\.(larksuite|feishu)\.(com|cn)/);
  return m ? m[1] : '';
}

function bail(value) {
  if (isCancel(value)) {
    cancel('Cancelled.');
    process.exit(0);
  }
  return value;
}

async function ask(prompt) {
  const v = await prompt;
  return bail(v);
}

export function defaultAnswers({ defaultName = 'my-wiki' } = {}) {
  return {
    COMPANY_NAME: 'Acme Corp',
    COMPANY_TAGLINE: 'A startup doing something amazing',
    CEO_NAME: 'CEO',
    LARK_TENANT: 'acme',
    WIKI_SPACE_ID: 'REPLACE_WITH_SPACE_ID',
    WIKI_INDEX_NODE_ID: 'REPLACE_WITH_INDEX_NODE_ID',
    LARK_BASE_APP_TOKEN: '',
    BRAND_1_NAME: 'Acme Corp',
    BRAND_1_FULL: 'Acme Corp',
    BRAND_1_ROLE: 'Main entity',
    BRAND_1_ROLE_SHORT: 'Main',
    BRAND_1_NOTE: '',
    BRAND_2_NAME: '',
    BRAND_2_FULL: '',
    BRAND_2_ROLE: '',
    BRAND_2_ROLE_SHORT: '',
    BRAND_2_NOTE: '',
    PRODUCT_LIST: 'TBD',
    SALES_CHANNELS: 'TBD',
    DAILY_VOLUME: 'TBD',
    PRICING_NOTE: 'TBD',
    PRICING_RULES: 'TBD',
    CORE_VALUE_1: 'TBD',
    CORE_VALUE_2: 'TBD',
    CORE_VALUE_3: 'TBD',
    MISSION: 'TBD',
    VISION: 'TBD',
    VISION_YEAR: '2030',
    CONTEXT_NOTES: 'TBD',
    ENTITY_DECISION_RULES: 'TBD',
    ENTITY_SPLIT_RULES: 'TBD',
    PAYROLL_DAY: '5',
    HANDOVER_DAY: '25',
    ADMIN_GROUP: 'WikiAdmins',
    EDITOR_GROUP: 'WikiEditors',
    VIEWER_GROUP: 'WikiViewers',
    CONTRIBUTOR_GROUP_NAME: 'WikiContributor',
    REVIEWER_BOT_NAME: '@wiki-reviewer',
    REVIEWER_EMAIL: 'wiki@example.com',
    COUNT_SPACE_I: '0',
    COUNT_SPACE_II: '0',
    COUNT_SPACE_III: '0',
    COUNT_SPACE_IV: '0',
    STATUS_SPACE_I: 'TODO',
    STATUS_SPACE_II: 'TODO',
    STATUS_SPACE_III: 'TODO',
    STATUS_SPACE_IV: 'TODO',
    initGit: false,
  };
}

export async function runPrompts({ defaultName = 'my-wiki' } = {}) {
  intro(kleur.bgCyan().black(' create-lark-startup-wiki '));

  const companyName = await ask(text({
    message: 'Company name',
    placeholder: 'Acme Corp',
    validate: (v) => (!v || v.trim().length === 0) ? 'Required' : undefined,
  }));

  const companyTagline = await ask(text({
    message: 'Company tagline (1 sentence)',
    placeholder: 'A startup doing X',
    initialValue: '',
  }));

  const ceoName = await ask(text({
    message: 'CEO / Founder name',
    placeholder: 'Jane Doe',
    initialValue: 'CEO',
  }));

  const wikiUrl = await ask(text({
    message: 'Lark Wiki Space URL',
    placeholder: 'https://acme.larksuite.com/wiki/space/7123456789',
    initialValue: '',
  }));
  const wikiSpaceId = parseWikiSpaceId(wikiUrl) || 'REPLACE_WITH_SPACE_ID';
  const larkTenant = parseTenant(wikiUrl) || 'acme';

  const indexNodeId = await ask(text({
    message: 'INDEX node ID (optional — paste node id of your TOC page)',
    placeholder: 'UxOkwdRyBi7oBLkFM5WlABIyg8g',
    initialValue: '',
  }));

  const hasIndexBase = await ask(confirm({
    message: 'Do you have a Lark Base for INDEX (canonical page list)?',
    initialValue: false,
  }));
  let indexBaseToken = '';
  if (hasIndexBase) {
    const baseUrl = await ask(text({
      message: 'Lark Base URL',
      placeholder: 'https://acme.larksuite.com/base/Bas123abc',
      initialValue: '',
    }));
    indexBaseToken = parseBaseAppToken(baseUrl);
  }

  const hasMultipleBrands = await ask(confirm({
    message: 'Multiple brands / legal entities?',
    initialValue: false,
  }));

  const brand1 = { NAME: companyName, FULL: companyName, ROLE: 'Main entity', ROLE_SHORT: 'Main', NOTE: '' };
  const brand2 = { NAME: '', FULL: '', ROLE: '', ROLE_SHORT: '', NOTE: '' };

  if (hasMultipleBrands) {
    brand1.NAME = await ask(text({ message: 'Brand 1 name (e.g. Production arm)', initialValue: companyName }));
    brand1.FULL = await ask(text({ message: 'Brand 1 full legal name', initialValue: brand1.NAME }));
    brand1.ROLE = await ask(text({ message: 'Brand 1 role', placeholder: 'Production — warehouse, factory, QC', initialValue: 'Production' }));
    brand1.ROLE_SHORT = await ask(text({ message: 'Brand 1 short role', initialValue: 'Production' }));

    brand2.NAME = await ask(text({ message: 'Brand 2 name (e.g. Commerce arm)', initialValue: '' }));
    brand2.FULL = await ask(text({ message: 'Brand 2 full legal name', initialValue: brand2.NAME }));
    brand2.ROLE = await ask(text({ message: 'Brand 2 role', placeholder: 'Commerce — sales, marketing, HR, accounting', initialValue: 'Commerce' }));
    brand2.ROLE_SHORT = await ask(text({ message: 'Brand 2 short role', initialValue: 'Commerce' }));
  }

  const initGit = await ask(confirm({
    message: 'Initialize a git repo in the new directory?',
    initialValue: true,
  }));

  outro(kleur.green('Got it. Generating your repo...'));

  const defaults = defaultAnswers({ defaultName });
  return {
    ...defaults,
    COMPANY_NAME: companyName,
    COMPANY_TAGLINE: companyTagline || defaults.COMPANY_TAGLINE,
    CEO_NAME: ceoName || defaults.CEO_NAME,
    LARK_TENANT: larkTenant,
    WIKI_SPACE_ID: wikiSpaceId,
    WIKI_INDEX_NODE_ID: indexNodeId || 'REPLACE_WITH_INDEX_NODE_ID',
    LARK_BASE_APP_TOKEN: indexBaseToken,
    BRAND_1_NAME: brand1.NAME,
    BRAND_1_FULL: brand1.FULL,
    BRAND_1_ROLE: brand1.ROLE,
    BRAND_1_ROLE_SHORT: brand1.ROLE_SHORT,
    BRAND_1_NOTE: brand1.NOTE,
    BRAND_2_NAME: brand2.NAME,
    BRAND_2_FULL: brand2.FULL,
    BRAND_2_ROLE: brand2.ROLE,
    BRAND_2_ROLE_SHORT: brand2.ROLE_SHORT,
    BRAND_2_NOTE: brand2.NOTE,
    initGit,
  };
}
