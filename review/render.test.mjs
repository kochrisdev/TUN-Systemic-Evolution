import test from 'node:test';
import assert from 'node:assert/strict';
import { renderReport } from './render.mjs';

function fixture() {
  const proposal = { id: 'p1', version: '1', action: 'Publish adoption manifest', target: 'local catalog',
    actor: { id: 'owner', name: 'Fixture owner', type: 'human' }, consequence: 'C3', effect: 'One local publication',
    authority: 'Current permission required', recovery: { kind: 'compensatable', description: 'History remains' } };
  const receipt = { id: 'r1', action: 'Publish adoption manifest', target: 'local catalog', actor: proposal.actor,
    timestamp: '2026-10-02T12:00:00Z', status: 'pending-verification', summary: 'Readback unavailable; outcome unknown.',
    verification: { state: 'unavailable', detail: 'Readback unavailable.' }, recovery: proposal.recovery };
  const before = { schemaVersion: 'tun-family-review/0.1', caseId: 'case1', sourceRevisions: { design: 'fixture' },
    management: { state: 'active', budget: { reservedMinor: 100, currency: 'USD' } },
    evolution: { assessment: 'supported', activation: null, activationStillCurrent: false, evidenceChanged: false },
    engineering: { operationId: 'op1', providerEffects: 1 }, design: { proposal, approvalStatus: 'approved', receipt },
    limitations: ['Synthetic evidence only.'] };
  const after = structuredClone(before);
  after.design.receipt.status = 'completed';
  after.design.receipt.summary = 'Manifest publication verified.';
  after.design.receipt.verification = { state: 'verified', detail: 'Bound local provider effect observed.' };
  after.evolution.activation = { id: 'activation1' };
  after.evolution.activationStillCurrent = true;
  return { schemaVersion: 'tun-family-demo/0.1', before, after, checks: {} };
}

test('real Design components preserve pending and completed receipts with disabled decisions', async () => {
  const html = await renderReport(fixture());
  assert.match(html, /tun-approval/);
  assert.match(html, /tun-receipt/);
  assert.match(html, /Readback unavailable/);
  assert.match(html, /Manifest publication verified/);
  assert.match(html, /Activation is a separate observation/);
  assert.equal((html.match(/<button[^>]*disabled=""/g) ?? []).length, 2);
  assert.doesNotMatch(html, /<script|@import/);
});

test('untrusted text is escaped by React', async () => {
  const report = fixture();
  report.after.design.proposal.contentPreview = '<script>alert("test")</script>';
  const html = await renderReport(report);
  assert.match(html, /&lt;script&gt;/);
  assert.doesNotMatch(html, /<script/);
});

test('mismatched case snapshots and unsupported versions are refused', async () => {
  const report = fixture();
  report.after.caseId = 'other-case';
  await assert.rejects(renderReport(report), /mismatched/);
  report.schemaVersion = 'future';
  await assert.rejects(renderReport(report), /Unsupported/);
});

test('publication alone never renders configuration activation as established', async () => {
  const report = fixture();
  report.after.evolution.activation = null;
  report.after.evolution.activationStillCurrent = false;
  const html = await renderReport(report);
  assert.match(html, /No Evolution activation has been recorded/);
  assert.match(html, /not established as current/);
});
