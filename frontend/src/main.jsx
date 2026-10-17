import React,{useEffect,useMemo,useState} from "react";
import {createRoot} from "react-dom/client";
import axios from "axios";
import {
  Activity,AlertTriangle,ArrowUpRight,BarChart3,Bell,Building2,CheckCircle2,
  ChevronRight,CircleHelp,Database,Download,FileCheck2,FileSearch,FileText,
  Filter,Info,LayoutDashboard,Search,Settings,ShieldCheck,UploadCloud,X,Zap,
  Clock,RefreshCw,Sparkles,Lightbulb,Target
} from "lucide-react";
import {
  AreaChart,Area,BarChart,Bar,CartesianGrid,XAxis,YAxis,Tooltip,
  ResponsiveContainer
} from "recharts";
import "./styles.css";

const API=import.meta.env.VITE_API_URL||"http://127.0.0.1:8000/api";
const api=axios.create({baseURL:API,timeout:8000});

function App(){
  const[tab,setTab]=useState("dashboard");
  const[summary,setSummary]=useState({});
  const[companies,setCompanies]=useState([]);
  const[reports,setReports]=useState([]);
  const[metrics,setMetrics]=useState([]);
  const[flags,setFlags]=useState([]);
  const[selectedFlag,setSelectedFlag]=useState(null);
  const[selectedCompany,setSelectedCompany]=useState(null);
  const[search,setSearch]=useState("");
  const[loading,setLoading]=useState(true);
  const[errors,setErrors]=useState([]);
  const[uploading,setUploading]=useState(false);

  const load=async()=>{
    setLoading(true);setErrors([]);
    const jobs=[
      ["summary",()=>api.get("/dashboard/summary"),r=>setSummary(r.data||{})],
      ["companies",()=>api.get("/companies"),r=>setCompanies(r.data||[])],
      ["reports",()=>api.get("/reports"),r=>setReports(r.data||[])],
      ["metrics",()=>api.get("/metrics"),r=>setMetrics(r.data||[])],
      ["flags",()=>api.get("/flags"),r=>setFlags(r.data||[])]
    ];
    const failed=[];
    for(const[name,request,setter]of jobs){
      try{setter(await request())}
      catch(e){failed.push(name)}
    }
    setErrors(failed);setLoading(false);
  };

  useEffect(()=>{load()},[]);

  const companyById=useMemo(
    ()=>Object.fromEntries(companies.map(c=>[c.id,c])),
    [companies]
  );
  const reportById=useMemo(
    ()=>Object.fromEntries(reports.map(r=>[r.id,r])),
    [reports]
  );
  const filteredCompanies=useMemo(
    ()=>companies.filter(c=>!search||`${c.name} ${c.sector} ${c.industry}`.toLowerCase().includes(search.toLowerCase())),
    [companies,search]
  );
  const filteredMetrics=useMemo(
    ()=>metrics.filter(m=>!search||`${m.metric_name} ${m.raw_unit}`.toLowerCase().includes(search.toLowerCase())),
    [metrics,search]
  );

  const upload=async p=>{
    setUploading(true);setErrors([]);
    try{
      const fd=new FormData();
      fd.append("file",p.file);
      fd.append("company_name",p.companyName);
      fd.append("sector",p.sector||"Unknown");
      fd.append("industry",p.industry||"Unknown");
      fd.append("identifier",p.identifier||"");
      fd.append("reporting_frequency",p.frequency);
      if(p.periodStart)fd.append("period_start",p.periodStart);
      if(p.periodEnd)fd.append("period_end",p.periodEnd);
      await api.post("/reports/upload",fd);
      await load();setTab("ingestion");
    }catch(e){setErrors(["upload"])}
    finally{setUploading(false)}
  };

  const nav=[
    ["dashboard","Executive Dashboard",LayoutDashboard],
    ["companies","Companies & Scope",Building2],
    ["investigation","Investigation",FileSearch],
    ["explorer","Normalized Data",Database],
    ["ingestion","Report Ingestion",UploadCloud]
  ];

  return <div className="platform-shell">
    <header className="platform-header">
      <div className="brand-block">
        <div className="brand-mark"><ShieldCheck size={21}/></div>
        <div><strong>PLAUSIBIL</strong><span>ESG DISCLOSURE MONITOR</span></div>
      </div>
      <div className="header-status"><span className="live-dot"/> Periodic anomaly engine <b>Active</b></div>
      <div className="header-actions">
        <button className="header-icon"><Bell size={17}/></button>
        <button className="header-icon"><Settings size={17}/></button>
      </div>
    </header>

    <div className="platform-body">
      <aside className="sidebar">
        <div className="sidebar-label">Platform Views</div>
        {nav.map(([id,label,Icon])=>
          <button key={id} className={`side-nav ${tab===id?"active":""}`} onClick={()=>setTab(id)}>
            <Icon size={16}/><span>{label}</span>
            {id==="investigation"&&flags.length>0&&<em>{flags.length}</em>}
          </button>
        )}
        <div className="sidebar-card">
          <div className="sidebar-card-title"><Zap size={14}/> Data cadence</div>
          <p>Weekly and monthly observations give the anomaly engine more temporal context than annual-only reporting.</p>
          <div className="cadence-row"><span>Weekly</span><b>{summary.weekly_reports||0}</b></div>
          <div className="cadence-row"><span>Monthly</span><b>{summary.monthly_reports||0}</b></div>
          <div className="cadence-row"><span>Annual</span><b>{summary.annual_reports||0}</b></div>
        </div>
      </aside>

      <main className="main-content">
        <div className="content-toolbar">
          <div className="global-search">
            <Search size={15}/>
            <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search companies or metrics..."/>
          </div>
          <button className="refresh-btn" onClick={load}><RefreshCw size={14}/> Refresh</button>
        </div>

        {errors.length>0&&
          <div className="error-banner">
            <AlertTriangle size={16}/>
            <span>Some Plausibil data could not be loaded: {errors.join(", ")}. Check the FastAPI terminal for details.</span>
            <button onClick={()=>setErrors([])}><X size={15}/></button>
          </div>
        }

        {loading&&<div className="loading-strip">Loading platform data…</div>}

        {tab==="dashboard"&&
          <Dashboard summary={summary} flags={flags} reports={reports} metrics={metrics}
            companies={companies}
            onFlag={f=>{setSelectedFlag(f);setTab("investigation")}}
            onUpload={p=>{setTab("ingestion");upload(p)}}/>
        }

        {tab==="companies"&&
          <Companies data={filteredCompanies} reports={reports} metrics={metrics} flags={flags}
            onOpen={c=>{setSelectedCompany(c);setTab("company")}}/>
        }

        {tab==="company"&&
          <CompanyDetail company={selectedCompany} reports={reports} metrics={metrics}
            flags={flags} onBack={()=>setTab("companies")}/>
        }

        {tab==="investigation"&&
          <InvestigationPage flags={flags} reports={reportById} companies={companyById}
            selected={selectedFlag} onOpen={setSelectedFlag}/>
        }

        {tab==="explorer"&&<DataExplorer data={filteredMetrics}/>}
        {tab==="ingestion"&&<Ingestion uploading={uploading} onUpload={upload}/>}
      </main>
    </div>
  </div>;
}

function PageTitle({eyebrow="SDG 13 · CLIMATE ACTION",title,subtitle,action}){
  return <div className="page-title">
    <div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{subtitle}</p></div>{action}
  </div>;
}

function KPI({icon:Icon,label,value,note,tone=""}){
  return <div className="kpi-card">
    <div className={`kpi-icon ${tone}`}><Icon size={17}/></div>
    <div><span>{label}</span><strong>{value??0}</strong>{note&&<small>{note}</small>}</div>
  </div>;
}

function Dashboard({summary,flags,reports,metrics,companies,onFlag,onUpload}){
  const trend=useMemo(()=>{
    const groups={};
    metrics.filter(m=>m.metric_name==="total_ghg_emissions").forEach(m=>{
      const r=reports.find(x=>x.id===m.report_id);
      if(!r?.period_end)return;
      groups[r.period_end]=(groups[r.period_end]||0)+Number(m.normalized_value??m.raw_value??0);
    });
    return Object.entries(groups).sort((a,b)=>a[0].localeCompare(b[0])).slice(-18)
      .map(([period,value])=>({period:period.slice(0,7),value:Math.round(value)}));
  },[metrics,reports]);

  const sectors=useMemo(()=>{
    const groups={};
    metrics.filter(m=>m.metric_name==="total_ghg_emissions").forEach(m=>{
      const r=reports.find(x=>x.id===m.report_id);
      const c=companies.find(x=>x.id===r?.company_id);
      if(c)(groups[c.sector]||=[]).push(Number(m.normalized_value??0));
    });
    return Object.entries(groups)
      .map(([sector,values])=>({sector,value:Math.round(values.reduce((a,b)=>a+b,0)/values.length)}))
      .sort((a,b)=>b.value-a.value).slice(0,5);
  },[metrics,reports,companies]);

  return <div className="page-view">
    <PageTitle title="Executive Dashboard"
      subtitle="Evidence-first monitoring of corporate sustainability disclosures across periodic and annual observations."
      action={
        <button className="primary-btn" onClick={()=>document.getElementById("dashboard-file")?.click()}>
          <UploadCloud size={15}/> Ingest report
          <input id="dashboard-file" hidden type="file" accept=".pdf"
            onChange={e=>{const f=e.target.files?.[0];if(f)onUpload({file:f,companyName:"Uploaded Company",frequency:"monthly"});e.target.value=""}}/>
        </button>
      }
    />

    <section className="kpi-grid">
      <KPI icon={Building2} label="Monitored entities" value={summary.companies} note={`${summary.reports||0} observations`}/>
      <KPI icon={FileCheck2} label="Periodic reports" value={summary.reports} note={`${summary.monthly_reports||0} monthly · ${summary.weekly_reports||0} weekly`} tone="blue"/>
      <KPI icon={AlertTriangle} label="Review signals" value={summary.flags} note={`${summary.high_priority||0} high priority`} tone="amber"/>
      <KPI icon={ShieldCheck} label="Normalized metrics" value={summary.metrics} note="Raw + normalized provenance" tone="slate"/>
    </section>

    <section className="dashboard-grid main-grid">
      <div className="card chart-card">
        <div className="card-head">
          <div><h2>Periodic emissions trend</h2><p>Aggregate normalized total GHG emissions across available reporting periods</p></div>
          <span className="chip">More observations → better temporal context</span>
        </div>
        <div className="chart-area">
          {trend.length?
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={trend}>
                <defs><linearGradient id="fill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#1f9d73" stopOpacity=".2"/>
                  <stop offset="100%" stopColor="#1f9d73" stopOpacity=".01"/>
                </linearGradient></defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#edf0f4"/>
                <XAxis dataKey="period" tickLine={false} axisLine={false} tick={{fontSize:10,fill:"#718096"}}/>
                <YAxis tickLine={false} axisLine={false} tick={{fontSize:10,fill:"#718096"}}/>
                <Tooltip/>
                <Area type="monotone" dataKey="value" stroke="#1f9d73" strokeWidth={2.5} fill="url(#fill)"/>
              </AreaChart>
            </ResponsiveContainer>
            :<Empty text="No dated observations yet."/>
          }
        </div>
        <div className="chart-foot">
          <span><b>{reports.length}</b> reporting observations</span>
          <span>Signals are prompts for human review, not findings of wrongdoing.</span>
        </div>
      </div>

      <div className="card">
        <div className="card-head"><div><h2>Recent review flags</h2><p>Source-level checks to investigate</p></div><ArrowUpRight size={16}/></div>
        <div className="flag-list">
          {flags.slice(0,6).length?
            flags.slice(0,6).map(f=><FlagRow key={f.id} flag={f} reports={reports} companies={companies} onClick={onFlag}/>)
            :<Empty text="No review signals yet."/>
          }
        </div>
      </div>
    </section>

    <section className="dashboard-grid lower-grid">
      <div className="card">
        <div className="card-head"><div><h2>Sector emissions footprint</h2><p>Average normalized total GHG emissions by sector</p></div><BarChart3 size={16}/></div>
        <div className="mini-chart">
          {sectors.length?
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={sectors}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#edf0f4"/>
                <XAxis dataKey="sector" tickLine={false} axisLine={false} tick={{fontSize:9,fill:"#667085"}}/>
                <YAxis tickLine={false} axisLine={false} tick={{fontSize:9,fill:"#667085"}}/>
                <Tooltip/><Bar dataKey="value" fill="#315d8b" radius={[5,5,0,0]}/>
              </BarChart>
            </ResponsiveContainer>
            :<Empty text="No sector data."/>
          }
        </div>
      </div>

      <div className="card">
        <div className="card-head"><div><h2>Data quality</h2><p>Extraction and normalization status</p></div><FileCheck2 size={16}/></div>
        <Quality metrics={metrics}/>
      </div>

      <div className="card">
        <div className="card-head"><div><h2>Cadence strategy</h2><p>Model training context</p></div><Clock size={16}/></div>
        <div className="cadence-panel">
          <div><b>Weekly</b><span>Fast operational changes</span></div>
          <div><b>Monthly</b><span>Core monitoring cadence</span></div>
          <div><b>Annual</b><span>Long-form disclosure anchor</span></div>
          <p>Periodic data is used as additional observations; it does not replace annual disclosures.</p>
        </div>
      </div>
    </section>
  </div>;
}

function Quality({metrics}){
  const valid=metrics.filter(m=>["VALID","NORMALIZED"].includes(m.data_quality_status)).length;
  const amb=metrics.filter(m=>m.data_quality_status==="AMBIGUOUS").length;
  const low=metrics.filter(m=>m.data_quality_status==="LOW_CONFIDENCE").length;
  return <div className="quality-grid">
    <div><b>{valid}</b><span>Valid / normalized</span></div>
    <div><b>{low}</b><span>Low confidence</span></div>
    <div><b>{amb}</b><span>Ambiguous</span></div>
  </div>;
}

function FlagRow({flag,reports,companies,onClick}){
  const r=reports.find(x=>x.id===flag.report_id);
  const c=companies.find(x=>x.id===r?.company_id);
  return <button className="flag-row" onClick={()=>onClick(flag)}>
    <span className={`priority ${flag.severity==="HIGH PRIORITY"?"high":"review"}`}>
      {flag.severity==="HIGH PRIORITY"?"High":"Review"}
    </span>
    <span><b>{c?.name||"Company"}</b><small>{flag.title}</small></span>
    <span className="flag-date">{r?.period_end||"—"}</span>
  </button>;
}

function Companies({data,reports,metrics,flags,onOpen}){
  return <div className="page-view">
    <PageTitle title="Companies & Scope" subtitle="Organizations, reporting cadence and source history across the monitoring dataset."/>
    <div className="card table-card">
      <div className="table-toolbar"><span>{data.length} monitored entities</span><span className="muted">Click Open for period-level detail</span></div>
      <table><thead><tr><th>Company</th><th>Sector</th><th>Observations</th><th>Review signals</th><th>Latest period</th><th/></tr></thead>
        <tbody>{data.map(c=>{
          const rs=reports.filter(r=>r.company_id===c.id);
          const fs=flags.filter(f=>rs.some(r=>r.id===f.report_id));
          return <tr key={c.id}>
            <td><b>{c.name}</b><small>{c.industry}</small></td><td>{c.sector}</td><td>{rs.length}</td><td>{fs.length}</td>
            <td>{rs[0]?.period_end||"—"}</td>
            <td><button className="table-link" onClick={()=>onOpen(c)}>Open <ChevronRight size={13}/></button></td>
          </tr>
        })}</tbody>
      </table>
    </div>
  </div>;
}

function CompanyDetail({company,reports,metrics,flags,onBack}){
  const rs=reports.filter(r=>r.company_id===company?.id);
  const ids=new Set(rs.map(r=>r.id));
  const ms=metrics.filter(m=>ids.has(m.report_id));
  const fs=flags.filter(f=>ids.has(f.report_id));
  const trend=rs.slice().reverse().map(r=>({
    period:(r.period_end||"").slice(0,7),
    value:ms.filter(m=>m.report_id===r.id&&m.metric_name==="total_ghg_emissions")
      .reduce((a,m)=>a+Number(m.normalized_value||0),0)
  })).filter(x=>x.period);

  return <div className="page-view">
    <button className="back-link" onClick={onBack}>← Companies</button>
    <PageTitle eyebrow="COMPANY PROFILE" title={company?.name||"Company"} subtitle={`${company?.sector||"—"} · ${company?.industry||"—"}`}/>
    <section className="kpi-grid">
      <KPI icon={FileText} label="Observations" value={rs.length}/>
      <KPI icon={Database} label="Metrics" value={ms.length}/>
      <KPI icon={AlertTriangle} label="Review signals" value={fs.length} tone="amber"/>
      <KPI icon={Activity} label="Cadence" value={rs[0]?.reporting_frequency||"—"}/>
    </section>
    <div className="card chart-card">
      <div className="card-head"><div><h2>Company periodic trajectory</h2><p>More frequent observations reveal changes between annual disclosures.</p></div></div>
      <div className="chart-area"><ResponsiveContainer width="100%" height={260}>
        <AreaChart data={trend}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#edf0f4"/>
          <XAxis dataKey="period" tickLine={false} axisLine={false}/>
          <YAxis tickLine={false} axisLine={false}/><Tooltip/>
          <Area dataKey="value" type="monotone" stroke="#315d8b" fill="#315d8b18"/>
        </AreaChart>
      </ResponsiveContainer></div>
    </div>
    <DataExplorer data={ms}/>
  </div>;
}

function DataExplorer({data}){
  return <div className="page-view">
    <PageTitle title="Normalized Data" subtitle="Raw values remain visible alongside normalized units for auditability."
      action={<a className="secondary-btn" href={`${API}/metrics/export.csv`}><Download size={14}/> Export CSV</a>}/>
    <div className="card table-card"><div className="table-scroll">
      <table><thead><tr><th>Metric</th><th>Report</th><th>Raw</th><th>Normalized</th><th>Page</th><th>Confidence</th><th>Quality</th></tr></thead>
      <tbody>{data.map(m=><tr key={m.id}>
        <td><b>{m.metric_name}</b></td><td>#{m.report_id}</td>
        <td>{m.raw_value??"—"} {m.raw_unit}</td>
        <td>{m.normalized_value??"—"} {m.normalized_unit}</td>
        <td>{m.page_number??"—"}</td>
        <td>{Math.round((m.extraction_confidence||0)*100)}%</td>
        <td><span className="quality-pill">{m.data_quality_status}</span></td>
      </tr>)}</tbody></table>
    </div></div>
  </div>;
}

function InvestigationPage({flags,reports,companies,selected,onOpen}){
  const active=selected&&flags.some(f=>f.id===selected.id)?selected:flags[0];
  const activeReport=active?reports[active.report_id]:null;
  const activeCompany=activeReport?companies[activeReport.company_id]:null;

  return <div className="page-view">
    <PageTitle title="Investigation" subtitle="Explainable review signals with source-level provenance."/>
    <div className="investigation-layout">
      <div className="card flag-explorer">
        <div className="card-head"><div><h2>Flag explorer</h2><p>Unusual or inconsistent observations for human review.</p></div><Filter size={16}/></div>
        {flags.map(f=><button className={`explorer-row ${active?.id===f.id?"selected":""}`} key={f.id} onClick={()=>onOpen(f)}>
          <span className={`priority-dot ${f.severity==="HIGH PRIORITY"?"high":""}`}/>
          <span><b>{f.title}</b><small>{f.flag_type} · score {Number(f.score||0).toFixed(2)}</small></span>
          <ChevronRight size={14}/>
        </button>)}
        {!flags.length&&<Empty text="No flags yet."/>}
      </div>
      <div className="card investigation-panel">
        {active?<Investigation key={active.id} flag={active} report={activeReport} company={activeCompany}/>:<Empty text="Select a review signal."/>}
      </div>
    </div>
  </div>;
}

function SeverityBadge({severity}){
  const high=severity==="HIGH PRIORITY";
  return <span className={`severity-badge ${high?"high":""}`}>
    <AlertTriangle size={12}/>{high?"High Priority":"Review"}
  </span>;
}

function Investigation({flag,report,company}){
  const[evidence,setEvidence]=useState(null);
  const[explanation,setExplanation]=useState(null);
  const[reviewed,setReviewed]=useState(false);
  const[busy,setBusy]=useState(true);
  const[loadError,setLoadError]=useState("");

  useEffect(()=>{
    let mounted=true;
    setBusy(true);setLoadError("");
    Promise.allSettled([
      api.get(`/flags/${flag.id}/evidence`),
      api.get(`/flags/${flag.id}/explanation`)
    ]).then(results=>{
      if(!mounted)return;
      if(results[0].status==="fulfilled")setEvidence(results[0].value.data);
      else setLoadError("Evidence could not be loaded. Check the FastAPI terminal.");
      if(results[1].status==="fulfilled")setExplanation(results[1].value.data);
      else setLoadError(prev=>prev||"Explanation could not be loaded. Check the FastAPI terminal.");
      setBusy(false);
    });
    return()=>{mounted=false};
  },[flag.id]);

  const items=evidence?.evidence||[];
  const primary=items.find(x=>x.page_number||x.source_text)||items[0];
  const triggered=explanation?.triggered_checks||[{
    name:String(flag.flag_type||"Review signal").replace(/_/g," "),
    status:"TRIGGERED",detail:flag.description
  }];
  const model=explanation?.model_explanation||{};
  const modelItems=Array.isArray(model.features)?model.features:[];
  const mitigation=Array.isArray(explanation?.mitigation?.actions)?explanation.mitigation.actions:[];

  const exportBrief=()=>{
    const text=[
      "PLAUSIBIL — INVESTIGATION BRIEF","",
      `Flag: ${flag.id}`,`Company: ${company?.name||"—"}`,
      `Report: ${report?.file_name||"—"}`,`Period: ${report?.period_end||"—"}`,
      `Severity: ${flag.severity}`,`Score: ${Number(flag.score||0).toFixed(2)}`,"",
      "OVERALL ASSESSMENT",explanation?.rule_explanation||flag.description,"",
      "TRIGGERED CHECKS",
      ...triggered.map(t=>`- ${t.name}: ${t.status}${t.detail?` — ${t.detail}`:""}`),"",
      "MODEL EXPLANATION",
      modelItems.length
        ?modelItems.map(f=>`- ${f.feature}: value ${Number(f.value).toFixed(3)}, baseline ${Number(f.baseline).toFixed(3)}, contribution ${Number(f.contribution).toFixed(3)} — ${f.interpretation}`).join("\n")
        :(model.note||"No local model explanation available."),"",
      "MITIGATION / RESOLUTION ACTIONS",
      ...mitigation.map(a=>`- ${a.action} (${a.owner}): ${a.detail}`),"",
      "SOURCE EVIDENCE",
      `Page: ${primary?.page_number??"—"}`,
      `Table: ${primary?.table_reference||"—"}`,
      `Raw value: ${primary?.raw_value??"—"} ${primary?.raw_unit||""}`,
      `Normalized value: ${primary?.normalized_value??"—"} ${primary?.normalized_unit||""}`,
      primary?.source_text||"No source text available.","",
      "Review signal only: validate the source report, boundaries, methodology and operational context before drawing conclusions."
    ].join("\n");

    const blob=new Blob([text],{type:"text/plain"});
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;a.download=`plausibil-audit-brief-${flag.id}.txt`;
    a.click();URL.revokeObjectURL(url);
  };

  return <div className="investigation-content">
    <div className="investigation-head">
      <div>
        <div className="eyebrow">AUDIT INVESTIGATION</div>
        <div className="title-line"><h2>{flag.title}</h2><SeverityBadge severity={flag.severity}/></div>
        <p>{company?.name||"Company"} · {flag.flag_type} · {report?.period_end||"Period unavailable"}</p>
      </div>
      <div className="investigation-actions">
        <button className="secondary-btn" onClick={()=>setReviewed(v=>!v)}>
          <CheckCircle2 size={14}/>{reviewed?"Reviewed":"Mark as Reviewed"}
        </button>
        <button className="dark-btn" onClick={exportBrief}><Download size={14}/> Export Audit Brief</button>
      </div>
    </div>

    {loadError&&<div className="inline-warning"><AlertTriangle size={14}/>{loadError}</div>}

    <div className="assessment-box">
      <div className="section-kicker"><ShieldCheck size={14}/> Overall Assessment</div>
      <p>{explanation?.rule_explanation||flag.description}</p>
      <small>Review signal only — this does not establish wrongdoing.</small>
    </div>

    <div className="investigation-grid reference-grid">
      <div className="investigation-left">

        <section className="investigation-section">
          <SectionTitle title="What Happened?"/>
          <p>This observation triggered <b>{flag.flag_type.replaceAll("_"," ")}</b>. Plausibil surfaces this signal so a reviewer can verify the underlying disclosure, reporting boundary, methodology, units and operational context.</p>
        </section>

        <section className="investigation-section">
          <SectionTitle title="Supporting Evidence"/>
          <div className="evidence-metrics">
            <EvidenceMetric label="Report" value={report?.file_name||"—"}/>
            <EvidenceMetric label="Period" value={report?.period_end||"—"}/>
            <EvidenceMetric label="Page" value={primary?.page_number??"—"}/>
            <EvidenceMetric label="Table" value={primary?.table_reference||"—"}/>
          </div>
        </section>

        <section className="investigation-section">
          <SectionTitle title="Triggered Checks"/>
          <div className="checks-list">
            {triggered.map((t,i)=><div className="check-row" key={i}>
              <span className="check-status failed">{t.status}</span>
              <div><b>{t.name}</b><span>{t.detail||"Rule result attached to this review signal."}</span></div>
            </div>)}
          </div>
        </section>

        <section className="investigation-section shap-section">
          <SectionTitle
            title="SHAP / Model Explanation"
            subtitle="Local feature contributions show which observed features influenced this anomaly model's output. They are not probabilities."
          />

          {modelItems.length?<>
            <div className="shap-summary">
              <div><Sparkles size={16}/><div>
                <b>{model.method||"SHAP TreeExplainer"}</b>
                <span>{model.observation_count||"—"} complete observations used for the fitted model.</span>
              </div></div>
              <span className="model-version">{model.model_version||"Isolation Forest"}</span>
            </div>

            <div className="shap-list">
              {modelItems.map((item,i)=>{
                const contribution=Number(item.contribution||0);
                const mag=Math.min(100,Math.max(8,Math.abs(contribution)*100));
                return <div className="shap-card" key={i}>
                  <div className="shap-card-head">
                    <div>
                      <b>{item.feature}</b>
                      <span>Observed {Number(item.value).toFixed(3)} · baseline {Number(item.baseline).toFixed(3)}</span>
                    </div>
                    <strong className={contribution>0?"positive":"negative"}>
                      {contribution>0?"+":""}{contribution.toFixed(3)}
                    </strong>
                  </div>
                  <div className="shap-track"><span style={{width:`${mag}%`}}/></div>
                  <p>{item.interpretation}</p>
                </div>;
              })}
            </div>

            {model.note&&<div className="model-note"><Info size={14}/>{model.note}</div>}
          </>:<div className="model-empty">
            <Sparkles size={17}/>
            <div>
              <b>Local SHAP explanation is not available for this flag</b>
              <p>{model.note||"The anomaly model needs enough complete historical observations for a stable local explanation."}</p>
            </div>
          </div>}
        </section>

        <section className="investigation-section mitigation-section">
          <SectionTitle
            title="Mitigation & Resolution Suggestions"
            subtitle="Practical review actions suggested from the detected inconsistency. These are not automatic corrections."
          />

          {mitigation.length?
            <div className="mitigation-list">
              {mitigation.map((item,i)=><div className="mitigation-card" key={i}>
                <div className="mitigation-icon"><Lightbulb size={16}/></div>
                <div className="mitigation-body">
                  <div className="mitigation-head"><b>{item.action}</b><span>{item.owner}</span></div>
                  <p>{item.detail}</p>
                </div>
                <span className="step-number">{item.step}</span>
              </div>)}
            </div>
            :<div className="model-empty">
              <Target size={17}/><div><b>No mitigation suggestions returned</b><p>Review the source evidence and reporting context manually.</p></div>
            </div>
          }
        </section>
      </div>

      <aside className="source-card reference-source">
        <div className="source-top">
          <div><div className="section-kicker">SOURCE EVIDENCE</div><h3>{company?.name||"Company"}</h3><p>{report?.file_name||"Report"}</p></div>
          <span className="confidence-chip">
            Confidence {primary?.extraction_confidence!=null?`${Math.round(primary.extraction_confidence*100)}%`:"—"}
          </span>
        </div>

        <div className="source-meta">
          <span>Reporting period<b>{report?.period_end||"—"}</b></span>
          <span>Cadence<b>{report?.reporting_frequency||"—"}</b></span>
        </div>

        <div className="source-code">
          <div className="source-code-head">[SOURCE EXTRACTION]</div>
          <pre>{primary?.source_text||"No source text was attached to this flag."}</pre>
        </div>

        <div className="evidence-values">
          <div><span>Raw value</span><b>{primary?.raw_value??"—"} {primary?.raw_unit||""}</b></div>
          <div><span>Normalized</span><b>{primary?.normalized_value??"—"} {primary?.normalized_unit||""}</b></div>
        </div>

        <div className="provenance">
          <span>Report</span><ChevronRight size={12}/><span>Page {primary?.page_number??"—"}</span>
          <ChevronRight size={12}/><span>{primary?.table_reference||"Table"}</span>
          <ChevronRight size={12}/><span>Metric</span>
        </div>

        <div className="source-note">
          <CircleHelp size={14}/>
          <span>The evidence panel shows data currently attached to the flag. It does not invent missing PDF text.</span>
        </div>
      </aside>
    </div>

    <div className="disclaimer">
      <ShieldCheck size={15}/>
      <span><b>Human review required.</b> An anomaly or validation failure is a prompt to inspect the disclosure, not a conclusion about the company.</span>
    </div>

    {busy&&<div className="loading-strip">
      <RefreshCw size={14} className="spin"/> Loading evidence, SHAP explanation and mitigation suggestions…
    </div>}
  </div>;
}

function SectionTitle({title,subtitle}){
  return <div className="section-title">
    <h3>{title}</h3>{subtitle&&<p>{subtitle}</p>}
  </div>;
}

function EvidenceMetric({label,value}){
  return <div className="evidence-metric"><span>{label}</span><b>{value}</b></div>;
}

function Ingestion({uploading,onUpload}){
  const[file,setFile]=useState(null);
  const[companyName,setCompanyName]=useState("");
  const[sector,setSector]=useState("");
  const[frequency,setFrequency]=useState("monthly");
  const[start,setStart]=useState("");
  const[end,setEnd]=useState("");

  const submit=()=>file&&onUpload({
    file,companyName:companyName||"Uploaded Company",
    sector,frequency,periodStart:start,periodEnd:end
  });

  return <div className="page-view">
    <PageTitle title="Report Ingestion" subtitle="Add weekly, monthly, quarterly or annual observations to build a denser time series."/>
    <div className="card ingestion-card">
      <div className="ingestion-copy">
        <UploadCloud size={36}/><h2>Upload a sustainability report</h2>
        <p>PDF extraction → unit normalization → rule checks → periodic anomaly analysis → evidence linkage.</p>
      </div>

      <div className="ingestion-form">
        <label>Company name<input value={companyName} onChange={e=>setCompanyName(e.target.value)} placeholder="Example Industries"/></label>
        <label>Sector<input value={sector} onChange={e=>setSector(e.target.value)} placeholder="Manufacturing"/></label>
        <label>Reporting cadence<select value={frequency} onChange={e=>setFrequency(e.target.value)}>
          <option value="weekly">Weekly</option><option value="monthly">Monthly</option>
          <option value="quarterly">Quarterly</option><option value="annual">Annual</option>
        </select></label>
        <label>Period start<input type="date" value={start} onChange={e=>setStart(e.target.value)}/></label>
        <label>Period end<input type="date" value={end} onChange={e=>setEnd(e.target.value)}/></label>
        <label className="file-picker">PDF file<input type="file" accept=".pdf" onChange={e=>setFile(e.target.files?.[0]||null)}/></label>
        <button className="primary-btn full" disabled={!file||uploading} onClick={submit}>
          {uploading?<><RefreshCw size={14}/> Processing…</>:<><UploadCloud size={14}/> Start ingestion</>}
        </button>
      </div>

      <div className="pipeline">
        <div><CheckCircle2 size={15}/> PDF / OCR extraction</div>
        <div><CheckCircle2 size={15}/> Metric normalization</div>
        <div><CheckCircle2 size={15}/> Internal consistency checks</div>
        <div><CheckCircle2 size={15}/> Periodic anomaly model</div>
        <div><CheckCircle2 size={15}/> Evidence linkage</div>
      </div>
    </div>
  </div>;
}

function Empty({text}){
  return <div className="empty"><Database size={22}/><span>{text}</span></div>;
}

createRoot(document.getElementById("root")).render(<App/>);