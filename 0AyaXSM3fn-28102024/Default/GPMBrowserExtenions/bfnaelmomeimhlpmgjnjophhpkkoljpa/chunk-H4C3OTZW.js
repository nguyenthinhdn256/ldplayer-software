import{a as y}from"./chunk-TISYHGD5.js";import{c as h,p as B,q as w}from"./chunk-PCKXDRQ7.js";import{o as t,qb as T,rb as k}from"./chunk-WIQ4WVKX.js";import{Bb as f,Na as x,vd as u}from"./chunk-MHD4HNLY.js";import{S as g}from"./chunk-6E74REJW.js";import{a as s}from"./chunk-7X4NV6OJ.js";import{f as d,h as r,n}from"./chunk-3KENBVE7.js";r();n();var m=d(s()),I=m.default.memo(({networkID:e,backgroundColor:i="white",...o})=>{let c=`Network${x.getChainName(e)}`;return c in h?m.default.createElement(w,{...o,icon:c,shape:"square",backgroundColor:i}):null});r();n();r();n();var p=d(s());r();n();var l=d(s());var C=({text:e})=>l.default.createElement(D,null,l.default.createElement(P,null,e)),N=t.div`
  display: flex;
  align-items: center;
`,D=t.div`
  background: ${g("#FFFFFF",.1)};
  border-radius: 3px;
  padding: 0px 4px;
  color: white;
  display: inline-block;
  margin-left: 5px;
`,P=t(T).attrs({size:12,lineHeight:17,weight:600,noWrap:!0})``;var Z=({children:e,networkID:i,walletAddress:o})=>p.default.createElement(N,null,e,o?p.default.createElement(W,{networkID:i,address:o}):null),W=({networkID:e,address:i})=>{let o=b({networkID:e,address:i});return o?p.default.createElement(C,{text:o}):null},_=({networkID:e,address:i})=>{let o=b({networkID:e,address:i});return o?p.default.createElement(B,{children:o,size:"small"}):null},b=({networkID:e,address:i})=>{let o=u();return f.get(e).badge?.(e,o,i)??null};r();n();var v=t.div`
  flex: 1;
  overflow: auto;
  padding: 20px 0;
`,pe=t(v)`
  padding-top: 0;
  padding-bottom: 0;
`,ae=t.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  padding: ${e=>e.size==="medium"?"20px":"30px"} 0 0;
`,de=t.section`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  > svg {
    margin-bottom: 16px;
  }
  > p {
    margin-bottom: 16px;
  }
`,se=t(k).attrs({size:16,lineHeight:22,weight:500,color:"#AB9FF2"})``,z=t.section`
  width: 100%;
  flex: 1;
  > * {
    margin-bottom: 10px;
  }
`,me=t(y).attrs({color:"#181818",diameter:94,includeDarkBoxShadow:!0})``,le=t.form`
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  ${z} {
    margin-top: 30px;
  }
`;export{I as a,D as b,Z as c,W as d,_ as e,v as f,pe as g,ae as h,de as i,se as j,z as k,me as l,le as m};
//# sourceMappingURL=chunk-H4C3OTZW.js.map
