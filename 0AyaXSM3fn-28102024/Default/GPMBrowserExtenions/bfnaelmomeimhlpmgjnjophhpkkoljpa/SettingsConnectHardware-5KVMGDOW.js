import{a as F,c as L,d as N,g as D}from"./chunk-JGDK6WWY.js";import{a as f}from"./chunk-MW3WETP7.js";import"./chunk-BXQ2FNBC.js";import"./chunk-EGECEZLM.js";import"./chunk-LCJF24CY.js";import{a as $}from"./chunk-T27XGMXK.js";import"./chunk-UMDV4H54.js";import"./chunk-XJWRT6N6.js";import"./chunk-GR6D4DPI.js";import"./chunk-NYONBW6F.js";import"./chunk-QBZHFUZ3.js";import"./chunk-CCUXU2GU.js";import"./chunk-BT2EXIW3.js";import"./chunk-6DOWJ64L.js";import"./chunk-Z6IB25YE.js";import"./chunk-QEXGR5WT.js";import"./chunk-YCCYNAY3.js";import"./chunk-NDHIYOGB.js";import{a as _}from"./chunk-X3ESGVCB.js";import"./chunk-Y3NV75FH.js";import"./chunk-S24UABH5.js";import"./chunk-SHAEZV7V.js";import"./chunk-H4C3OTZW.js";import"./chunk-DERIAD33.js";import"./chunk-EGXLQXDH.js";import"./chunk-CCQRCL2K.js";import{e as T}from"./chunk-I5YT3SXD.js";import{a as m}from"./chunk-TISYHGD5.js";import"./chunk-BRWGJFNS.js";import"./chunk-IVMV7P4T.js";import"./chunk-JCHDEXQW.js";import{a as g}from"./chunk-BBDLE433.js";import"./chunk-P7NGDOTF.js";import"./chunk-HPOS2V3B.js";import"./chunk-XYJX6G2K.js";import"./chunk-3WUBIQFW.js";import"./chunk-W27Z2YZM.js";import"./chunk-PCKXDRQ7.js";import"./chunk-H3FFS4GT.js";import"./chunk-NSMHSELH.js";import"./chunk-YHY2IGPI.js";import"./chunk-PTZMRZUV.js";import"./chunk-VQVTLSDS.js";import{a as P,b as O}from"./chunk-OKP6DFCI.js";import{o as c,v as E}from"./chunk-WIQ4WVKX.js";import"./chunk-LTUJMY6D.js";import"./chunk-UCBZOSRF.js";import"./chunk-PN7XAO7F.js";import"./chunk-TZKYPSN2.js";import"./chunk-36Y64SHT.js";import"./chunk-2MSBWT3V.js";import"./chunk-NM5XY6LY.js";import"./chunk-AKPGU3DO.js";import"./chunk-IS26EKBL.js";import"./chunk-GQEPK4C4.js";import"./chunk-BTKBODVJ.js";import"./chunk-KXAUXXVB.js";import"./chunk-TYXPKGSM.js";import"./chunk-WFPABEAU.js";import"./chunk-QWOVPA54.js";import"./chunk-LDMZMUWY.js";import"./chunk-X2SBUKU4.js";import"./chunk-OXFZHPMY.js";import"./chunk-EDLKLLZ5.js";import"./chunk-OX7Q6J2U.js";import{Fd as v,Nd as B}from"./chunk-MHD4HNLY.js";import"./chunk-G3SOTMUM.js";import"./chunk-56SJOU6P.js";import{g as y}from"./chunk-6E74REJW.js";import"./chunk-N7UFQNLW.js";import"./chunk-66TF6S77.js";import"./chunk-4P36KWOF.js";import{a as H}from"./chunk-7X4NV6OJ.js";import"./chunk-UNDMYLJW.js";import{f as b,h as r,n}from"./chunk-3KENBVE7.js";r();n();var o=b(H());r();n();var i=b(H());r();n();var G=c(m)`
  cursor: pointer;
  width: 24px;
  height: 24px;
  transition: background-color 200ms ease;
  background-color: ${t=>t.$isExpanded?"#000":"#333"} !important;
  :hover {
    background-color: #444444;
    svg {
      fill: white;
    }
  }
  svg {
    fill: ${t=>t.$isExpanded?"white":"#666666"};
    transition: fill 200ms ease;
    position: relative;
    ${t=>t.top?`top: ${t.top}px;`:""}
    ${t=>t.right?`right: ${t.right}px;`:""}
  }
`;var U=c(_).attrs({justify:"space-between"})`
  background-color: #222222;
  padding: 10px 16px;
  border-bottom: 1px solid #323232;
  height: 46px;
  opacity: ${t=>t.opacity??"1"};
`,V=c.div`
  display: flex;
  margin-left: 10px;
  > * {
    margin-right: 10px;
  }
`,I=c.div`
  width: 24px;
  height: 24px;
`,M=({onBackClick:t,totalSteps:a,currentStepIndex:p,isHidden:l,showBackButtonOnFirstStep:e,showBackButton:u=!0})=>i.default.createElement(U,{opacity:l?0:1},u&&(e||p!==0)?i.default.createElement(G,{right:1,onClick:t},i.default.createElement(E,null)):i.default.createElement(I,null),i.default.createElement(V,null,y(a).map(s=>{let d=s<=p?"#AB9FF2":"#333";return i.default.createElement(m,{key:s,diameter:12,color:d})})),i.default.createElement(I,null));r();n();var z=()=>{let{mutateAsync:t}=B(),{hardwareStepStack:a,pushStep:p,popStep:l,currentStep:e,setOnConnectHardwareAccounts:u,setOnConnectHardwareDone:w,setExistingAccounts:s}=F(),{data:d=[],isFetched:x,isError:k}=v(),C=T(a,(h,J)=>h?.length===J.length),W=a.length>(C??[]).length,A=C?.length===0,X={initial:{x:A?0:W?150:-150,opacity:A?1:0},animate:{x:0,opacity:1},exit:{opacity:0},transition:{duration:.2}},j=(0,o.useCallback)(()=>{e()?.props.preventBack||(e()?.props.onBackCallback&&e()?.props.onBackCallback?.(),l())},[e,l]);return $(()=>{u(async h=>{await t(h),await g.set(f,!await g.get(f))}),w(()=>self.close()),p(o.default.createElement(D,null))},a.length===0),(0,o.useEffect)(()=>{s({data:d,isFetched:x,isError:k})},[d,x,k,s]),o.default.createElement(L,null,o.default.createElement(M,{totalSteps:3,onBackClick:j,showBackButton:!e()?.props.preventBack,currentStepIndex:a.length-1}),o.default.createElement(O,{mode:"wait"},o.default.createElement(P.div,{style:{display:"flex",flexGrow:1},key:`${a.length}_${C?.length}`,...X},o.default.createElement(N,null,e()))))},yt=z;export{yt as default};
//# sourceMappingURL=SettingsConnectHardware-5KVMGDOW.js.map
