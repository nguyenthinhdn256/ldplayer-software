import{a as Z}from"./chunk-LEECQOCO.js";import{a as $}from"./chunk-QGXEKSEY.js";import{a as F}from"./chunk-SD2WCJUI.js";import{a as G}from"./chunk-2WECCVZD.js";import{Ra as j,wa as B,ya as U}from"./chunk-GR6D4DPI.js";import{k as Q}from"./chunk-NYONBW6F.js";import"./chunk-QBZHFUZ3.js";import"./chunk-CCUXU2GU.js";import"./chunk-BT2EXIW3.js";import"./chunk-6DOWJ64L.js";import"./chunk-Z6IB25YE.js";import"./chunk-QEXGR5WT.js";import"./chunk-YCCYNAY3.js";import"./chunk-NDHIYOGB.js";import{a as x}from"./chunk-X3ESGVCB.js";import"./chunk-Y3NV75FH.js";import"./chunk-S24UABH5.js";import"./chunk-SHAEZV7V.js";import"./chunk-H4C3OTZW.js";import{g as O}from"./chunk-DERIAD33.js";import"./chunk-EGXLQXDH.js";import{a as V}from"./chunk-CCQRCL2K.js";import"./chunk-I5YT3SXD.js";import"./chunk-TISYHGD5.js";import"./chunk-BRWGJFNS.js";import{a as z}from"./chunk-IVMV7P4T.js";import"./chunk-P7NGDOTF.js";import"./chunk-HPOS2V3B.js";import"./chunk-XYJX6G2K.js";import"./chunk-3WUBIQFW.js";import"./chunk-W27Z2YZM.js";import{D as A,G as E,a as P,b as D}from"./chunk-PCKXDRQ7.js";import"./chunk-H3FFS4GT.js";import"./chunk-NSMHSELH.js";import"./chunk-YHY2IGPI.js";import"./chunk-PTZMRZUV.js";import"./chunk-VQVTLSDS.js";import{j as _}from"./chunk-OKP6DFCI.js";import{D as N,o as s,rb as w}from"./chunk-WIQ4WVKX.js";import"./chunk-LTUJMY6D.js";import"./chunk-UCBZOSRF.js";import{$ as v,T as W,ba as L,ca as k,j as M}from"./chunk-PN7XAO7F.js";import"./chunk-TZKYPSN2.js";import"./chunk-36Y64SHT.js";import"./chunk-2MSBWT3V.js";import"./chunk-NM5XY6LY.js";import"./chunk-AKPGU3DO.js";import"./chunk-IS26EKBL.js";import"./chunk-GQEPK4C4.js";import"./chunk-BTKBODVJ.js";import"./chunk-KXAUXXVB.js";import"./chunk-TYXPKGSM.js";import"./chunk-WFPABEAU.js";import"./chunk-QWOVPA54.js";import"./chunk-LDMZMUWY.js";import"./chunk-X2SBUKU4.js";import"./chunk-OXFZHPMY.js";import"./chunk-EDLKLLZ5.js";import"./chunk-OX7Q6J2U.js";import{Wd as H}from"./chunk-MHD4HNLY.js";import"./chunk-G3SOTMUM.js";import{m as p}from"./chunk-56SJOU6P.js";import"./chunk-6E74REJW.js";import"./chunk-N7UFQNLW.js";import"./chunk-66TF6S77.js";import"./chunk-4P36KWOF.js";import{a as T}from"./chunk-7X4NV6OJ.js";import"./chunk-UNDMYLJW.js";import{f as y,h as S,n as I}from"./chunk-3KENBVE7.js";S();I();var t=y(T());S();I();var o=y(T());var K=P({marginLeft:4}),X=s(x).attrs({align:"center",padding:"10px"})`
  background-color: #2a2a2a;
  border-radius: 6px;
  height: 74px;
  margin: 4px 0;
`,Y=s.div`
  display: flex;
  align-items: center;
`,R=s(V)`
  flex: 1;
  min-width: 0;
  text-align: left;
  align-items: normal;
`,tt=s(w).attrs({size:16,weight:600,lineHeight:19,noWrap:!0,maxWidth:"175px",textAlign:"left"})``,et=s(w).attrs({color:"#777777",size:14,lineHeight:17,noWrap:!0})`
  text-align: left;
  margin-top: 5px;
`,ot=s.div`
  width: 55px;
  min-width: 55px;
  max-width: 55px;
  height: 55px;
  min-height: 55px;
  max-height: 55px;
  aspect-ratio: 1;
  margin-right: 10px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
`,q=o.default.memo(e=>{let{t:n}=p(),{collection:i,unknownItem:m,isHidden:r,isSpam:a,onToggleHidden:d}=e,{name:c,id:h}=i,l=L(i),g=l?.chainData,f=k(i),u=v(l?.media,"image",!1,"small"),C=c||l?.name||m;return o.default.createElement(X,null,o.default.createElement(ot,null,a&&r?o.default.createElement(Z,{width:32}):u?o.default.createElement(U,{uri:u}):M(g)?o.default.createElement($,{...g.utxoDetails}):o.default.createElement(B,{type:"image",width:42})),o.default.createElement(x,null,o.default.createElement(R,null,o.default.createElement(Y,null,o.default.createElement(tt,null,C),a?o.default.createElement(N,{className:K,fill:D.colors.legacy.accentWarning,height:16,width:16}):null),o.default.createElement(et,null,n("collectiblesSearchNrOfItems",{nrOfItems:f})))),o.default.createElement(G,{id:h,label:`${c} visible`,checked:!r,onChange:b=>{d(b.target.checked?"show":"hide")}}))});var it=74,nt=10,lt=it+nt,st=20,rt=s.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
`,at=s.div`
  position: relative;
  width: 100%;
`,mt=()=>{let{handleHideModalVisibility:e}=j(),{data:n,isPending:i}=H(),{viewState:m,viewStateLoading:r}=W({account:n}),a=(0,t.useCallback)(()=>e("collectiblesVisibility"),[e]),d=(0,t.useMemo)(()=>({...m,handleCloseModal:a}),[a,m]),c=(0,t.useMemo)(()=>i||r,[i,r]);return{data:d,loading:c}},ct=t.default.memo(e=>{let{t:n}=p(),i=(0,t.useRef)(null);return(0,t.useEffect)(()=>{setTimeout(()=>i.current?.focus(),200)},[]),t.default.createElement(t.default.Fragment,null,t.default.createElement(at,null,t.default.createElement(O,{ref:i,tabIndex:0,placeholder:n("assetListSearch"),maxLength:50,onChange:e.handleSearch,value:e.searchQuery,name:"Search collectibles"})),t.default.createElement(Q,null,t.default.createElement(A,null,({height:m,width:r})=>t.default.createElement(E,{style:{padding:`${st}px 0`},scrollToIndex:e.searchQuery!==e.debouncedSearchQuery?0:void 0,height:m,width:r,rowCount:e.listItems.length,rowHeight:lt,rowRenderer:a=>t.default.createElement(dt,{...a,data:e.listItems,unknownItem:n("assetListUnknownToken"),getIsHidden:e.getIsHidden,getIsSpam:e.getIsSpam,getSpamStatus:e.getSpamStatus,onToggleHidden:e.onToggleHidden})}))))}),dt=e=>{let{index:n,data:i,style:m,unknownItem:r,getIsHidden:a,getIsSpam:d,getSpamStatus:c,onToggleHidden:h}=e,l=i[n],g=a(l),f=d(l),u=c(l),C=(0,t.useCallback)(b=>h({item:l,status:b}),[h,l]);return t.default.createElement("div",{style:m},t.default.createElement(q,{collection:l,unknownItem:r,isHidden:g,isSpam:f,spamStatus:u,onToggleHidden:C}))},pt=()=>{let{data:e,loading:n}=mt(),{t:i}=p();return t.default.createElement(rt,null,n?t.default.createElement(F,null):t.default.createElement(ct,{...e}),t.default.createElement(z,null,t.default.createElement(_,{onClick:e.handleCloseModal},i("commandClose"))))},Ut=pt;export{pt as CollectiblesVisibilityPage,Ut as default};
//# sourceMappingURL=CollectiblesVisibilityPage-6VFYA5RV.js.map
