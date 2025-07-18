import{b as s}from"./chunk-PTZMRZUV.js";import{_ as l,o as t,rb as w}from"./chunk-WIQ4WVKX.js";import{t as x}from"./chunk-2MSBWT3V.js";import{b as d,c as y}from"./chunk-NM5XY6LY.js";import{d as g}from"./chunk-IS26EKBL.js";import{m as b}from"./chunk-56SJOU6P.js";import{A as i,sa as k}from"./chunk-66TF6S77.js";import{a as F}from"./chunk-7X4NV6OJ.js";import{f as P,h as E,n as h}from"./chunk-3KENBVE7.js";E();h();var r=P(F());var T="Unknown Error",B="Looks like you ran into an unknown error. Please close Phantom and try again.",D="Close",f=t(w).attrs({wordBreak:"break-word",color:"#777777",size:16,lineHeight:20.8,maxWidth:"400px"})``,m=t.a.attrs({target:"_blank",rel:"noopener noreferrer"})`
  display: flex;
  align-items: center;
  margin: 0 auto;
  color: #ab9ff2;
  text-decoration: none;
  cursor: pointer;
  svg {
    fill: #ab9ff2;
    margin-right: 5px;
  }
`,u=class extends r.default.Component{constructor(o){super(o),this.state={error:null}}static getDerivedStateFromError(o){return o instanceof Error?{error:o}:typeof o=="string"?{error:new Error(o)}:{error:new Error}}componentDidCatch(o,a){o instanceof Error&&k.captureError(o,"generic")}render(){return this.state.error?typeof this.props.fallback=="function"?this.props.fallback(this.state.error):this.props.fallback:this.props.children}},C=n=>r.default.createElement(u,{fallback:o=>o instanceof x?r.default.createElement(S,null):n.fallback},n.children),S=()=>{let{t:n}=b(),o=()=>{g.capture("walletScreenErrorBoundaryClosed"),self.close()};return r.default.createElement(A,null,r.default.createElement(s,{icon:"error",title:n("transactionsDisabledTitle"),buttonText:n("commandClose"),onClose:o},r.default.createElement(f,{margin:"0 0 5px 0"},n("transactionsDisabledMessage")),r.default.createElement(m,{href:i,onClick:o},r.default.createElement(l,null),"Help & Support")))},A=t.main`
  width: ${d}px;
  height: ${y}px;
  padding: 15px;
`,X=({title:n=T,message:o=B,buttonText:a=D,onReset:e=()=>self.close(),children:c})=>{function p(){return r.default.createElement(H,null,r.default.createElement(s,{icon:"error",title:n,buttonText:a,onClose:e},r.default.createElement(f,{margin:"0 0 5px 0"},o),r.default.createElement(m,{href:i,onClick:e},r.default.createElement(l,null),"Help & Support")))}return r.default.createElement(C,{fallback:r.default.createElement(p,null)},c)},H=t.main`
  min-width: ${d}px;
  height: 100vh;
  padding: 15px;
  width: 100vw;
`,j=({title:n=T,message:o="Looks like you ran into an unknown error. Please refresh the page and try again.",buttonText:a="Refresh",onReset:e=()=>self.location.reload(),children:c})=>{function p(){return r.default.createElement(N,null,r.default.createElement(s,{icon:"error",title:n,buttonText:a,onClose:e},r.default.createElement(f,{margin:"0 0 5px 0"},o),r.default.createElement(m,{href:i,onClick:e},r.default.createElement(l,null),"Help & Support")))}return r.default.createElement(C,{fallback:r.default.createElement(p,null)},c)},N=t.main`
  width: 400px;
  height: 450px;
  background-color: #222222;
  border: 1px solid #323232;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  padding: 20px;
`;export{u as a,C as b,X as c,j as d};
//# sourceMappingURL=chunk-YHY2IGPI.js.map
