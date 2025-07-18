import{pa as E,ra as z,sa as H,ta as K,ua as V}from"./chunk-GR6D4DPI.js";import{a as x}from"./chunk-X3ESGVCB.js";import{a as W,k as pe}from"./chunk-H4C3OTZW.js";import{a as le,b as j}from"./chunk-DERIAD33.js";import{c as se,d as de,l as ce}from"./chunk-3WUBIQFW.js";import{f as D,q as N}from"./chunk-PCKXDRQ7.js";import{o as s,rb as v,u as L}from"./chunk-WIQ4WVKX.js";import{d as ae}from"./chunk-IS26EKBL.js";import{b as oe}from"./chunk-OX7Q6J2U.js";import{$d as ne,Bc as R,Bd as te,Id as re,Mb as Y,Na as b,ca as Q,ee as U,oe as ie,vd as B,xc as Z,yd as ee}from"./chunk-MHD4HNLY.js";import{m as y}from"./chunk-56SJOU6P.js";import{L as G,M as q,sa as J}from"./chunk-66TF6S77.js";import{a as P}from"./chunk-7X4NV6OJ.js";import{f as k,h as c,n as l}from"./chunk-3KENBVE7.js";c();l();var $=k(P());var Oe=e=>{let{t}=y(),o=Z(),{data:d=[]}=R(),{mutateAsync:i}=ne(),{mutateAsync:p}=re(),h=(0,$.useCallback)((T,I,S)=>{let u=d.find(w=>w.accountHash===T.identifier),A={name:u?.name??t("onboardingImportAccountsAccountName",{walletIndex:S+I+1})};return u?.icon&&(A.icon=u.icon.startsWith("https://")?{type:"image",imageUrl:u.icon}:{type:"emoji",unicode:u.icon}),A},[d,t]);return{handleImportSeed:(0,$.useCallback)(async(T,I,S,u=0)=>{let A={},w=await(e==="seed"?se(T,I,S):de(T,I,S));if(w.forEach((f,g)=>{A[f.identifier]=h(f,g,u)}),w.length===0)throw new Error("Failed to set seed phrase");await p({metadataBatch:A}),await i({identifier:w[0].identifier});try{await o.downloadSyncedAccounts()}catch{}try{let f=new Set;for(let g of w)g.type==="seedless"&&f.add(g.seedIdentifier);for(let g of[...f])await ce.addAuthFactor({secretIdentifier:g})}catch{J.captureError(new Error("Unable to add auth factor for se*dless account."),"Auth")}ae.capture("addSeedAccount",{data:{walletIndex:u+1}})},[h,p,i,e,o])}};c();l();var n=k(P());c();l();var r=k(P());var ue=({onChange:e,value:t,networkID:o})=>{let d=B(),i=(0,r.useMemo)(()=>{if(!o)return[];let h=b.getAddressTypes(o);return d.filter(m=>h.includes(m))},[d,o]);if(!i||i.length===0)return null;let p=i.includes(t)?t:i[0];return r.default.createElement(Ie,{onChange:e,value:p},({isExpanded:h})=>r.default.createElement(r.default.Fragment,null,r.default.createElement(Ce,{isActive:h},r.default.createElement(me,{networkID:o,addressType:p},r.default.createElement(fe,null,r.default.createElement(L,{fill:"#777",width:10})))),r.default.createElement(be,{portal:!1},r.default.createElement(K,{maxHeight:"300px"},i?.filter(m=>m!==p)?.map(m=>r.default.createElement(ve,{key:m,value:m},r.default.createElement(me,{networkID:o,addressType:m})))))))},me=({addressType:e,networkID:t,children:o})=>!t||!e?null:r.default.createElement(x,{justify:"space-between"},r.default.createElement(x,null,r.default.createElement(W,{networkID:t,size:32}),r.default.createElement(Te,null,Q.getDisplayName(e))),o),Ie=s(E)`
  width: 100%;
  position: relative;
`,fe=s.div`
  display: inline-flex;
  line-height: 0;
`,Ce=s(({isActive:e,...t})=>r.default.createElement(z,{...t}))`
  padding: 8px 16px 8px 12px;

  ${fe} {
    svg {
      transform: rotate(${e=>e.isActive?"-180deg":"0"});
      transition: transform 0.2s ease-in-out;
    }
  }
`,be=s(H)`
  z-index: 2;
  width: 100%;
`,ve=s(V)`
  padding: 8px 16px 8px 12px;
  min-height: 50px;
`,Te=s(v).attrs({size:16,weight:400,lineHeight:19,margin:"0 0 0 8px"})``;c();l();var a=k(P());var ke=s(E)`
  width: 100%;
  position: relative;
`,he=s.div`
  display: inline-flex;
  line-height: 0;
`,Pe=s(({isActive:e,...t})=>a.default.createElement(z,{...t}))`
  padding: 8px 16px 8px 12px;

  ${he} {
    svg {
      transform: rotate(${e=>e.isActive?"-180deg":"0"});
      transition: transform 0.2s ease-in-out;
    }
  }
`,De=s(H)`
  z-index: 2;
  width: 100%;
`,Ne=s(V)`
  padding: 8px 16px 8px 12px;
  min-height: 50px;
`,Fe=s(v).attrs({size:16,weight:400,lineHeight:19,margin:"0 0 0 8px"})``,Se=({onChange:e,value:t})=>{let o=ee();return a.default.createElement(ke,{onChange:e,value:t},({isExpanded:d})=>a.default.createElement(a.default.Fragment,null,a.default.createElement(Pe,{isActive:d},a.default.createElement(ye,{networkID:t},a.default.createElement(he,null,a.default.createElement(L,{fill:"#777",width:10})))),a.default.createElement(De,{portal:!1},a.default.createElement(K,{maxHeight:"300px"},o.filter(i=>i!==t).map(i=>a.default.createElement(Ne,{key:i,value:i},a.default.createElement(ye,{networkID:i})))))))},ye=({networkID:e,children:t})=>a.default.createElement(x,{justify:"space-between"},a.default.createElement(x,null,a.default.createElement(W,{networkID:e,size:32}),a.default.createElement(Fe,null,b.getNetworkName(e))),t);var zt=({onClick:e,disabled:t})=>{let{t:o}=y(),d=te();return n.default.createElement(D,{topLeft:{text:o("addAccountImportWalletPrimaryText"),font:"bodyMedium"},bottomLeft:{text:o(d?"addAccountImportWalletSolanaSecondaryText":"addAccountImportWalletSecondaryText")},start:n.default.createElement(N,{backgroundColor:"borderPrimary",color:"textPrimary",icon:"Download",shape:"circle",size:32}),onClick:e,disabled:t})},Ht=({control:e,getValues:t,register:o,setValue:d,trigger:i,errors:p,nameValidations:h,privateKey:m,privateKeyValidations:T,addressPreview:I})=>{let{t:S}=y(),u=ie(C=>C.editableAccountMetadata),A=t("networkID"),w=b.getAddressTypes(A),f=B(),g=f.filter(C=>w.includes(C));return n.default.createElement(pe,null,n.default.createElement(U,{name:"networkID",control:e,render:({field:{onChange:C,value:_}})=>f.length===1?n.default.createElement(n.default.Fragment,null):n.default.createElement(Se,{onChange:M=>{C(M);let we=b.getAddressTypes(M),ge=f.filter(xe=>we.includes(xe));d("addressType",ge[0]),m&&i("privateKey")},value:_})}),n.default.createElement(U,{name:"addressType",control:e,render:({field:{onChange:C,value:_}})=>g.length===1?n.default.createElement(n.default.Fragment,null):n.default.createElement(ue,{onChange:M=>{C(M),m&&i("privateKey")},value:_,networkID:A})}),n.default.createElement(j.WithWarning,{placeholder:S("addAccountImportAccountName"),defaultValue:u?.name,warning:!!p.name,warningMessage:p.name?.message,autoComplete:"off",maxLength:oe,...o("name",h)}),n.default.createElement(Ae.WithWarning,{placeholder:S("addAccountImportAccountPrivateKey"),defaultValue:"",warning:!!p.privateKey,warningMessage:p.privateKey?.message,autoComplete:"off",...o("privateKey",T)}),I?n.default.createElement(Me,{label:S("settingsWalletAddress"),pubkey:I}):null)},Me=n.default.memo(({label:e,pubkey:t})=>n.default.createElement(x,{justify:"space-between",align:"center",margin:"-7px 0 0"},n.default.createElement(v,{size:16,weight:600},e),n.default.createElement(v,{size:16},Y(t,4)))),Be=s(j.withComponent("textarea"))`
  height: 120px;
  text-align: start;
  resize: none;
  -webkit-text-security: disc;
`,Ae=le(Be);Ae.defaultProps={fontSize:"16px"};c();l();var O=k(P());var Ot=({onClick:e,disabled:t})=>{let{t:o}=y(),d=G||q;return O.default.createElement(D,{topLeft:{text:o("addAccountHardwareWalletPrimaryText"),font:"bodyMedium"},bottomLeft:{text:o("addAccountHardwareWalletSecondaryText")},start:O.default.createElement(N,{backgroundColor:"borderPrimary",color:"textPrimary",icon:"WalletHardware",shape:"circle",size:32}),onClick:e,disabled:t||d})};c();l();var X=k(P());var Yt=({onClick:e,disabled:t})=>{let{t:o}=y();return X.default.createElement(D,{topLeft:{text:o("addAccountImportSeedPhrasePrimaryText"),font:"bodyMedium"},bottomLeft:{text:o("addAccountImportSeedPhraseSecondaryText")},start:X.default.createElement(N,{backgroundColor:"borderPrimary",color:"textPrimary",icon:"File",shape:"circle",size:32}),onClick:e,disabled:t})};export{Oe as a,Se as b,zt as c,Ht as d,Ot as e,Yt as f};
//# sourceMappingURL=chunk-C46BLHWH.js.map
