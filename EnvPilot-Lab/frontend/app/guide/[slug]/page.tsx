import {readFile} from 'node:fs/promises';
import path from 'node:path';
import Link from 'next/link';
import {notFound} from 'next/navigation';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {guides,guideHref} from '../../../lib/guides';

export const dynamic='force-dynamic';

export default async function GuidePage({params}:{params:Promise<{slug:string}>}) {
  const {slug}=await params;
  const guide=guides.find(item=>item.slug===slug);
  if (!guide) notFound();
  const root=process.env.LAB_DOCS_DIR || path.resolve(process.cwd(),'..');
  let content:string;
  try {content=await readFile(path.join(root,guide.file),'utf8');}
  catch {return <main><h1>Guide files unavailable</h1><p>Recreate the web service with the updated Compose configuration, then reload this page.</p><code>docker compose up -d --build web</code><p><Link href="/">Return to dashboard</Link></p></main>;}
  return <main className="guide-page">
    <nav className="guide-nav" aria-label="Guide navigation"><Link href="/guide">← All exercises</Link><Link href="/">Dashboard</Link></nav>
    <div className="guide-layout">
      <aside aria-label="Guide sections"><p className="eyebrow">LEARNER GUIDE</p>{guides.map(item=><Link key={item.slug} href={`/guide/${item.slug}`} aria-current={item.slug===slug?'page':undefined}>{item.title}</Link>)}</aside>
      <article className="guide-document">
        <Markdown remarkPlugins={[remarkGfm]} skipHtml components={{
          a:({href,children})=>{
            const target=href?guideHref(guide.file,href):undefined;
            return target?<a href={target}>{children}</a>:<span>{children}</span>;
          }
        }}>{content}</Markdown>
      </article>
    </div>
  </main>;
}
