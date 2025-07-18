import{a as F}from"./chunk-SLD6KXWR.js";import{a as b}from"./chunk-L3H6M2JT.js";import{a as w}from"./chunk-5ARH2RW3.js";import"./chunk-FPRO5GQI.js";import"./chunk-BXQ2FNBC.js";import"./chunk-2WECCVZD.js";import"./chunk-L6RDTAJI.js";import"./chunk-UMDV4H54.js";import"./chunk-XJWRT6N6.js";import{Ra as T,z as x}from"./chunk-GR6D4DPI.js";import"./chunk-NYONBW6F.js";import"./chunk-QBZHFUZ3.js";import"./chunk-CCUXU2GU.js";import"./chunk-BT2EXIW3.js";import"./chunk-6DOWJ64L.js";import"./chunk-Z6IB25YE.js";import"./chunk-QEXGR5WT.js";import"./chunk-YCCYNAY3.js";import"./chunk-NDHIYOGB.js";import"./chunk-X3ESGVCB.js";import"./chunk-Y3NV75FH.js";import"./chunk-S24UABH5.js";import"./chunk-SHAEZV7V.js";import"./chunk-H4C3OTZW.js";import"./chunk-DERIAD33.js";import"./chunk-EGXLQXDH.js";import"./chunk-CCQRCL2K.js";import{h as g}from"./chunk-I5YT3SXD.js";import"./chunk-TISYHGD5.js";import"./chunk-BRWGJFNS.js";import{a as y}from"./chunk-IVMV7P4T.js";import"./chunk-P7NGDOTF.js";import"./chunk-HPOS2V3B.js";import"./chunk-XYJX6G2K.js";import"./chunk-3WUBIQFW.js";import"./chunk-W27Z2YZM.js";import"./chunk-PCKXDRQ7.js";import"./chunk-H3FFS4GT.js";import"./chunk-NSMHSELH.js";import"./chunk-YHY2IGPI.js";import"./chunk-PTZMRZUV.js";import"./chunk-VQVTLSDS.js";import{j as P}from"./chunk-OKP6DFCI.js";import{o as i}from"./chunk-WIQ4WVKX.js";import{Ja as R,Wa as h,Xa as C,ga as f,ma as v,ua as S}from"./chunk-LTUJMY6D.js";import"./chunk-UCBZOSRF.js";import"./chunk-PN7XAO7F.js";import"./chunk-TZKYPSN2.js";import"./chunk-36Y64SHT.js";import{v as c}from"./chunk-2MSBWT3V.js";import"./chunk-NM5XY6LY.js";import"./chunk-AKPGU3DO.js";import"./chunk-IS26EKBL.js";import"./chunk-GQEPK4C4.js";import"./chunk-BTKBODVJ.js";import"./chunk-KXAUXXVB.js";import"./chunk-TYXPKGSM.js";import"./chunk-WFPABEAU.js";import"./chunk-QWOVPA54.js";import"./chunk-LDMZMUWY.js";import"./chunk-X2SBUKU4.js";import"./chunk-OXFZHPMY.js";import"./chunk-EDLKLLZ5.js";import"./chunk-OX7Q6J2U.js";import{Wd as u}from"./chunk-MHD4HNLY.js";import"./chunk-G3SOTMUM.js";import{m as d}from"./chunk-56SJOU6P.js";import"./chunk-6E74REJW.js";import"./chunk-N7UFQNLW.js";import"./chunk-66TF6S77.js";import"./chunk-4P36KWOF.js";import{a as M}from"./chunk-7X4NV6OJ.js";import"./chunk-UNDMYLJW.js";import{f as I,h as l,n as m}from"./chunk-3KENBVE7.js";l();m();var e=I(M());var D=i.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  overflow-y: scroll;
  padding: 16px 16px ${78}px; // footer height + padding
`,E=i.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
`,H=i.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 16px;
  position: absolute;
  bottom: 0;
`,Q=i.div`
  background-color: #2a2a2a;
  border-radius: 6px;
  width: 100%;

  > *:first-child {
    border-bottom: 1px solid #222222;
  }
`,W=()=>{let{t}=d(),{handleHideModalVisibility:r}=T(),{pushDetailView:n}=g(),{resume:p}=v(),o=f(a=>a.quoteResponse),{data:s}=u(),V=(0,e.useMemo)(()=>s?.addresses.find(a=>a.networkID===o?.sellToken.chainId),[s,o]);(0,e.useEffect)(()=>{R()},[]),c(V,"SWAP_FUNGIBLE");let B=(0,e.useCallback)(()=>n(e.default.createElement(b,null)),[n]),k=S({goToConfirmation:B}),A=(0,e.useCallback)(()=>{p(),r("swapReview")},[r,p]);return{...k,hideSwapReview:A,t}},q=e.default.memo(({buyToken:t,sellToken:r,hideSwapReview:n,onSwap:p,t:o})=>{let{infoRowDisplayStrategy:s}=C();return e.default.createElement(D,null,e.default.createElement(E,null,e.default.createElement(x,{leftButton:{type:"close",onClick:n}},o("swapReviewFlowPrimaryText")),e.default.createElement(Q,null,e.default.createElement(w,{...r,title:o("swapReviewFlowYouPay")}),e.default.createElement(w,{...t,title:o("swapReviewFlowYouReceive")})),e.default.createElement(F,{isSwapReview:!0,rowDisplayStrategy:s})),e.default.createElement(H,null,e.default.createElement(y,{removeFooterExpansion:!0,removeShadowFooter:!0},e.default.createElement(P,{theme:"primary",onClick:p},o("swapReviewFlowActionButtonPrimary")))))}),N=()=>{let t=W();return e.default.createElement(h,null,e.default.createElement(q,{...t}))},Y=()=>e.default.createElement(N,null),ne=Y;export{Y as SwapReviewPage,ne as default};
//# sourceMappingURL=SwapReviewPage-FS7RWYRD.js.map
