import React,{useEffect,useState} from 'react'
import {Routes,Route,useLocation} from 'react-router-dom'
import {api,csrf} from './services/api'
import Navbar from './components/Navbar'
import Toast from './components/Toast'
import {Home,Stories,Story,Auth,Dashboard,BlogEditor,Profile,StaticPage,NotFound} from './pages'

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}
function Footer(){return <footer className="site-footer"><div className="container footer-inner"><div><Link className="brand footer-brand" to="/"> <span className="brand-mark">i.</span> ink & insight</Link><p>Thoughtful stories for curious minds.</p></div><div className="footer-links"><Link to="/stories">Explore</Link><Link to="/about">About</Link><Link to="/contact">Contact</Link></div><small>© {new Date().getFullYear()} Ink & Insight. Made for ideas worth sharing.</small></div></footer>}
import {Link} from 'react-router-dom'
export default function App(){
 const [user,setUser]=useState(null),[ready,setReady]=useState(false),[toast,setToast]=useState('')
 useEffect(()=>{csrf().then(()=>api.get('/auth/me/')).then(r=>setUser(r.data)).catch(()=>setUser(null)).finally(()=>setReady(true))},[])
 if(!ready)return <div className="app-loading"><div className="brand"><span className="brand-mark">i.</span> ink & insight</div><div className="spinner-border"/></div>
 return <><ScrollToTop/><Navbar user={user} setUser={setUser}/><Routes>
 <Route path="/" element={<Home/>}/><Route path="/stories" element={<Stories/>}/><Route path="/story/:slug" element={<Story user={user} setToast={setToast}/>}/>
 <Route path="/login" element={<Auth mode="login" setUser={setUser} setToast={setToast}/>}/><Route path="/register" element={<Auth mode="register" setUser={setUser} setToast={setToast}/>}/>
 <Route path="/dashboard" element={user?<Dashboard user={user} setToast={setToast}/>:<Auth mode="login" setUser={setUser} setToast={setToast}/>}/>
 <Route path="/write" element={user?<BlogEditor setToast={setToast}/>:<Auth mode="login" setUser={setUser} setToast={setToast}/>}/>
 <Route path="/edit/:slug" element={user?<BlogEditor edit setToast={setToast}/>:<Auth mode="login" setUser={setUser} setToast={setToast}/>}/>
 <Route path="/profile/:username" element={<Profile user={user} setToast={setToast}/>}/><Route path="/profile/edit" element={user?<Profile user={user} setToast={setToast} edit/>:<Auth mode="login" setUser={setUser} setToast={setToast}/>}/>
 <Route path="/about" element={<StaticPage type="about"/>}/><Route path="/contact" element={<StaticPage type="contact"/>}/><Route path="*" element={<NotFound/>}/>
 </Routes><Footer/><Toast message={toast} onClose={()=>setToast('')}/></>
}
