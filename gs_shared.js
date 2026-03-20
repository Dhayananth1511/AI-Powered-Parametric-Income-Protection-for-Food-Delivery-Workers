/* ── GigSecure Shared Store v2 ── */
const GS = {

  PLAN_META: {
    starter: { name:'🌱 Starter', price:55,  rate:35, maxHrs:3, cap:105 },
    basic:   { name:'🔵 Basic',   price:70,  rate:45, maxHrs:4, cap:180 },
    standard:{ name:'🟡 Standard',price:90,  rate:60, maxHrs:5, cap:300 },
    premium: { name:'🟠 Premium', price:115, rate:75, maxHrs:6, cap:450 },
    elite:   { name:'🔴 Elite',   price:135, rate:90, maxHrs:7, cap:630 },
  },

  SEED_WORKERS: [
    { id:'WKR-4821', name:'Ravi Kumar',     phone:'+91 98765 43210', email:'ravi.kumar@swiggy.in',    zone:'Velachery, Chennai',    pincode:'600042', platform:'Swiggy', plan:'standard', riskScore:0.58, trustScore:92, payouts:640,  simPayouts:0, claimsTotal:8,  weeklyHrsUsed:2, joined:'2026-01-12', role:'worker', password:'demo1234' },
    { id:'WKR-3302', name:'Arjun Raj',      phone:'+91 90123 45678', email:'arjun.raj@zomato.in',     zone:'Marina Beach, Chennai', pincode:'600005', platform:'Zomato', plan:'elite',    riskScore:0.85, trustScore:88, payouts:1200, simPayouts:0, claimsTotal:15, weeklyHrsUsed:3, joined:'2026-02-04', role:'worker', password:'demo1234' },
    { id:'WKR-7741', name:'Suresh Murugan', phone:'+91 87654 32109', email:'suresh.m@swiggy.in',      zone:'T. Nagar, Chennai',     pincode:'600017', platform:'Swiggy', plan:'basic',    riskScore:0.45, trustScore:61, payouts:270,  simPayouts:0, claimsTotal:4,  weeklyHrsUsed:1, joined:'2026-02-18', role:'worker', password:'demo1234' },
  ],

  SEED_ADMINS: [
    { id:'ADM-001', name:'Karthik Sundaram', email:'admin@digit.com',   password:'admin123', role:'admin', org:'Digit Insurance Pvt Ltd',   designation:'Portfolio Manager', phone:'+91 80000 00001', joined:'2026-01-01' },
    { id:'ADM-002', name:'Priya Nair',        email:'ops@gigsecure.in', password:'admin123', role:'admin', org:'GigSecure Platform Admin', designation:'Platform Admin',     phone:'+91 80000 00002', joined:'2026-01-01' },
  ],

  init(){
    if(!localStorage.getItem('gs_workers')) localStorage.setItem('gs_workers', JSON.stringify(this.SEED_WORKERS));
    if(!localStorage.getItem('gs_admins'))  localStorage.setItem('gs_admins',  JSON.stringify(this.SEED_ADMINS));
  },

  getWorkers(){ return JSON.parse(localStorage.getItem('gs_workers')||'[]'); },
  saveWorkers(ws){ localStorage.setItem('gs_workers', JSON.stringify(ws)); },
  addWorker(w){
    const ws=this.getWorkers();
    ws.push({payouts:0,simPayouts:0,claimsTotal:0,weeklyHrsUsed:0,...w});
    this.saveWorkers(ws);
  },
  updateWorker(id, patch){
    const ws=this.getWorkers();
    const idx=ws.findIndex(w=>w.id===id);
    if(idx>-1){ ws[idx]={...ws[idx],...patch}; this.saveWorkers(ws); }
    const cur=this.getCurrent();
    if(cur&&cur.id===id) this.setCurrent({...cur,...patch});
  },

  getAdmins(){ return JSON.parse(localStorage.getItem('gs_admins')||'[]'); },
  addAdmin(a){ const as=this.getAdmins(); as.push(a); localStorage.setItem('gs_admins',JSON.stringify(as)); },

  setCurrent(u){ localStorage.setItem('gs_current', JSON.stringify(u)); },
  getCurrent(){  return JSON.parse(localStorage.getItem('gs_current')||'null'); },
  logout(){ localStorage.removeItem('gs_current'); window.location.href='gigsecure_login.html'; },

  // Record a simulation payout — updates the worker's record in localStorage
  recordPayout(workerId, amount){
    const ws=this.getWorkers();
    const idx=ws.findIndex(w=>w.id===workerId);
    if(idx>-1){
      ws[idx].simPayouts  = (ws[idx].simPayouts||0) + amount;
      ws[idx].claimsTotal = (ws[idx].claimsTotal||0) + 1;
      this.saveWorkers(ws);
      const cur=this.getCurrent();
      if(cur&&cur.id===workerId) this.setCurrent({...cur, simPayouts:ws[idx].simPayouts, claimsTotal:ws[idx].claimsTotal});
    }
  },

  // Compute admin stats live from worker records
  getAdminStats(){
    const ws=this.getWorkers();
    const totalPrem   = ws.reduce((s,w)=>s+(this.PLAN_META[w.plan]?.price||79),0);
    const totalPayout = ws.reduce((s,w)=>s+(w.payouts||0)+(w.simPayouts||0),0);
    const totalClaims = ws.reduce((s,w)=>s+(w.claimsTotal||0),0);
    return {
      policies: ws.length,
      weeklyPremium: totalPrem,
      totalPayouts: totalPayout,
      platformFee: +(totalPrem*0.1).toFixed(1),
      totalClaims,
      newToday: ws.filter(w=>w.fresh).length,
      planBreakdown: ws.reduce((a,w)=>{ a[w.plan]=(a[w.plan]||0)+1; return a; },{}),
    };
  },

  fmt(n){ return '₹'+Number(n).toLocaleString('en-IN'); },
};
GS.init();