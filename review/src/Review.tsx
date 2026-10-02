import { ApprovalGate } from '../../vendor/design/packages/react/src/ApprovalGate.js';
import { ActionReceipt } from '../../vendor/design/packages/react/src/ActionReceipt.js';
import type { ActionProposal, ApprovalStatus, ReceiptData } from '../../vendor/design/packages/react/src/contracts.js';

interface Snapshot {
  caseId: string;
  sourceRevisions: Record<string, string>;
  management: { state: string; budget: { reservedMinor: number; currency: string } };
  evolution: { assessment: string; activation: { id: string } | null; activationStillCurrent: boolean; evidenceChanged: boolean };
  engineering: { operationId: string | null; providerEffects: number };
  design: { proposal: ActionProposal | null; approvalStatus: ApprovalStatus; receipt: ReceiptData | null };
  limitations: string[];
}

export interface FamilyReport {
  schemaVersion: 'tun-family-demo/0.1';
  before: Snapshot;
  after: Snapshot;
  checks: Record<string, boolean>;
}

const noDecision = () => { throw new Error('This report has no live decision endpoint.'); };

export function Review({ report }: { report: FamilyReport }) {
  const after = report.after;
  return <main>
    <header className="hero">
      <p className="kicker">TUN SYSTEMIC EVOLUTION · FAMILY PILOT</p>
      <h1>From shared learning<br />to a verified change.</h1>
      <p className="lead">A recorded Management decision, an Engineering publication, and an Evolution activation—shown through TUN Design.</p>
      <p className="notice">Read-only report. Synthetic evidence and fixture identities. No model or real participants were evaluated.</p>
    </header>
    <section aria-labelledby="path-title">
      <h2 id="path-title">One case, four responsibilities</h2>
      <div className="path">
        <article><span>01 · EVOLUTION</span><h3>Assess the candidate</h3><p>Current comparison: <strong>{after.evolution.assessment}</strong>.</p><p>{after.evolution.evidenceChanged ? 'Evidence changed since review.' : 'The reviewed evidence remains bound to the case.'}</p></article>
        <article><span>02 · MANAGEMENT</span><h3>Record the mandate</h3><p>Mandate: <strong>{after.management.state}</strong>.</p><p>{after.management.budget.currency} {(after.management.budget.reservedMinor / 100).toFixed(2)} reserved in fixture accounting; this is not measured spend.</p></article>
        <article><span>03 · ENGINEERING</span><h3>Verify the publication</h3><p>{after.engineering.providerEffects} local provider effect{after.engineering.providerEffects === 1 ? '' : 's'} recorded.</p><p>The publication receipt concerns the adoption manifest.</p></article>
        <article><span>04 · DESIGN</span><h3>Show what is known</h3><p>Proposal, uncertainty, and verified receipt retain their distinct meanings.</p><p>Local configuration: <strong>{after.evolution.activationStillCurrent ? 'activated and still current' : 'not established as current'}</strong>.</p></article>
      </div>
    </section>
    {after.design.proposal ? <section aria-labelledby="proposal-title"><h2 id="proposal-title">The reviewed action</h2>
      <ApprovalGate proposal={after.design.proposal} status={after.design.approvalStatus} approveLabel="Publish adoption manifest"
        blockedReason="Historical, read-only report. This page cannot authorize or execute an action." onDecision={noDecision} />
    </section> : null}
    <section aria-labelledby="evidence-title">
      <h2 id="evidence-title">A lost response stays unresolved until readback</h2>
      <div className="comparison">
        <article><h3>Before reconciliation</h3><p>The provider response was lost. Readback was unavailable, so the baseline remained active.</p>
          {report.before.design.receipt ? <ActionReceipt receipt={report.before.design.receipt} /> : <p>No action receipt is available.</p>}
        </article>
        <article><h3>After restart and reconciliation</h3><p>The original operation was verified without publishing a replacement.</p>
          {after.design.receipt ? <ActionReceipt receipt={after.design.receipt} /> : <p>No action receipt is available.</p>}
        </article>
      </div>
    </section>
    <section className="activation" aria-labelledby="activation-title"><h2 id="activation-title">Activation is a separate observation</h2>
      <p>{after.evolution.activation ? 'Evolution recorded the local configuration change after publication verification and current checks.' : 'No Evolution activation has been recorded.'}</p>
      <p>A completed publication receipt does not establish configuration activation, human learning, or customer benefit.</p>
      {after.evolution.activation ? <p className="identifier">Activation {after.evolution.activation.id}</p> : null}
    </section>
    <section aria-labelledby="limits-title"><h2 id="limits-title">Scope of this evidence</h2>
      <ul>{after.limitations.map(item => <li key={item}>{item}</li>)}</ul>
      <details><summary>Source revisions and case identifiers</summary>
        <dl>{Object.entries(after.sourceRevisions).map(([name, revision]) => <div key={name}><dt>{name}</dt><dd>{revision}</dd></div>)}</dl>
        <p className="identifier">Case {after.caseId}</p><p className="identifier">Operation {after.engineering.operationId ?? 'not recorded'}</p>
      </details>
    </section>
    <footer>Learn deliberately. Change responsibly. Evolve together.</footer>
  </main>;
}
