import Link from 'next/link';
import {guides} from '../../lib/guides';

export default function GuideIndex() {
  return <main className="guide-home"><header><div><p className="eyebrow">ENVPILOT LAB / LEARNER GUIDE</p><h1>Know what to do next.</h1></div><Link className="secondary-link" href="/">← Dashboard</Link></header>
    <section className="guide-intro"><p>Start with Day 1 and read the issue card before editing code. Use the dashboard to observe behavior and the terminal to run checks. Request a hint explicitly with <code>python lab.py hint &lt;exercise&gt; &lt;level&gt;</code>.</p><p>14 focused hours over two days, including an independent three-hour mock. Breaks are additional. Each exercise has a task, acceptance criteria, checks, and an engineering note.</p><Link className="primary-link" href="/guide/day-1">Start with Day 1 →</Link></section>
    {['Getting started','Exercises','Reference'].map(group=><section key={group} className="guide-group"><h2>{group}</h2><div className="guide-links">{guides.filter(guide=>guide.group===group).map(guide=><Link key={guide.slug} href={`/guide/${guide.slug}`}><span>{guide.title}</span><span aria-hidden="true">↗</span></Link>)}</div></section>)}
    <footer>The independent mock starts only when you explicitly run its CLI command. Browsing this guide does not start a timer.</footer>
  </main>;
}
