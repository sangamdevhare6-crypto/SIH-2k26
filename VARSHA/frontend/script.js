/* VARSHA KRITRIMA BUDHHIH - Django-backed authentication. */
const roles = {
  citizen:{title:'Citizen Login',welcome:'Welcome Citizen!',icon:'👥',desc:'Access rainfall alerts, safe routes and weather updates.',features:['🌧️ Live Rainfall Alerts','📍 Safety & Route Guidance','🌊 Inundation Updates','☁️ Weather Forecast'],color:'linear-gradient(100deg,#12a8ed,#167ff0)'},
  admin:{title:'Administrator Login',welcome:'Welcome Administrator!',icon:'⚙️',desc:'Manage users, monitoring sources, configuration and system access.',features:['👥 User Management','⚙️ System Configuration','📡 Data Sources','🔐 Audit & Access Control'],color:'linear-gradient(100deg,#7b61e8,#5367e8)'}
};
const params=new URLSearchParams(location.search), role=params.get('role');
if(role&&roles[role]){const c=roles[role]; const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};set('roleTitle',c.title);set('welcome',c.welcome);set('roleIcon',c.icon);set('roleDesc',c.desc);const b=document.getElementById('roleButton');if(b)b.style.background=c.color;const f=document.getElementById('roleFeatures');if(f)f.innerHTML=c.features.map(x=>`<div>${x}</div>`).join('')}
async function api(path,payload){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});let d={};try{d=await r.json()}catch{};if(!r.ok)throw new Error(d.message||'Request failed.');return d}
function redirectToDashboard(r){location.href=r==='admin'?'admin-dashboard.html':'citizen-dashboard.html'}
async function createAccount(e){e.preventDefault();const f=e.target,i=f.querySelectorAll('input'),role=f.querySelector('select').value;const data={fullName:i[0].value.trim(),email:i[1].value.trim().toLowerCase(),mobile:i[2].value.trim(),password:i[3].value,confirm:i[4].value,role};if(data.password!==data.confirm)return alert('Passwords do not match.');if(data.password.length<6)return alert('Password must contain at least 6 characters.');try{await api('/api/signup/',data);alert('Account created successfully! Please login.');location.href=`role-login.html?role=${role}`}catch(x){alert(x.message)}}
async function login(e){e.preventDefault();const f=e.target;try{const d=await api('/api/login/',{email:f.querySelector('input[type=email]').value.trim().toLowerCase(),password:f.querySelector('input[type=password]').value});redirectToDashboard(d.user.role)}catch(x){alert(x.message)}}
async function roleLogin(e){e.preventDefault();const f=e.target;try{const d=await api('/api/login/',{email:f.querySelector('input[type=email]').value.trim().toLowerCase(),password:f.querySelector('input[type=password]').value});if(role&&d.user.role!==role)return alert(`This account is registered as ${d.user.role}.`);redirectToDashboard(d.user.role)}catch(x){alert(x.message)}}
async function resetPassword(e){e.preventDefault();const np=document.getElementById('newPassword').value,cp=document.getElementById('confirmNewPassword').value;if(np!==cp)return alert('Passwords do not match.');try{await api('/api/reset-password/',{email:document.getElementById('resetEmail').value.trim().toLowerCase(),newPassword:np});alert('Password reset successfully. Please login again.');location.href='role-login.html'}catch(x){alert(x.message)}}
async function logout(){try{await api('/api/logout/',{})}finally{location.href='index.html'}}
async function protectDashboard(requiredRole){try{const r=await fetch('/api/me/');if(!r.ok)throw 0;const d=await r.json(),u=d.user;if(requiredRole&&u.role!==requiredRole)return redirectToDashboard(u.role);const id=requiredRole==='admin'?'adminName':'citizenName';const el=document.getElementById(id);if(el)el.textContent=u.name;return u}catch{alert('Please login first.');location.href='index.html'}}
if(document.body.classList.contains('dashboard-page')){const isAdmin=document.title.toLowerCase().includes('administrator');protectDashboard(isAdmin?'admin':'citizen')}


// Shared protection for the administrator sidebar pages.
if(document.body.classList.contains('admin-page')){
  protectDashboard('admin').then(u=>{
    const name=document.getElementById('profileName'); const email=document.getElementById('profileEmail');
    const ei=document.getElementById('profileEmailInput'); const fn=document.getElementById('profileFullName');
    if(name) name.textContent=u.name; if(email) email.textContent=u.email; if(ei) ei.value=u.email; if(fn) fn.value=u.name;
    const av=document.querySelector('.user-avatar'); if(av) av.textContent=(u.name||'A').charAt(0).toUpperCase();
  });
}
