import{a as P}from"./chunk-BXQ2FNBC.js";import{a as ct}from"./chunk-T27XGMXK.js";import{b as st,c as it,d as be}from"./chunk-UMDV4H54.js";import{a as K}from"./chunk-XJWRT6N6.js";import{e as me}from"./chunk-CCUXU2GU.js";import{a as ae,c as at}from"./chunk-H4C3OTZW.js";import{a as De}from"./chunk-3WUBIQFW.js";import{l as ot,m as nt}from"./chunk-W27Z2YZM.js";import{i as ce,j as B}from"./chunk-OKP6DFCI.js";import{Fa as rt,o as i,rb as _}from"./chunk-WIQ4WVKX.js";import{a as Ze}from"./chunk-LTUJMY6D.js";import{a as Re,l as et,x as ye}from"./chunk-36Y64SHT.js";import{Gb as Ae,Mb as Xe,Mc as Ce,Na as M,X as $e,Y as Ke,Z as Ye,ne as tt,ud as Je,vd as Se,wd as Qe,yd as we}from"./chunk-MHD4HNLY.js";import{K as _e}from"./chunk-G3SOTMUM.js";import{m as v}from"./chunk-56SJOU6P.js";import{D as Ue,d as ke,fa as Ve,ka as qe}from"./chunk-6E74REJW.js";import{$a as ze,Za as je}from"./chunk-66TF6S77.js";import{a as R}from"./chunk-7X4NV6OJ.js";import{f as Q,h as A,n as C}from"./chunk-3KENBVE7.js";A();C();var vt={existingAccounts:{data:[],isFetched:!1,isError:!1},hardwareStepStack:[],hardwareStepSubStack:{},selectedChains:[],selectedChainsMap:new Map,chainImportStep:1,derivedAccountGroups:[],discoveredAccounts:[],activeAccountsFound:!1,selectedAccounts:{},onConnectHardwareAccounts:e=>Promise.resolve(),onConnectHardwareDone:()=>{}},I=tt((e,o)=>({...vt,pushStep:t=>{let r=o().hardwareStepStack;e({hardwareStepStack:r.concat(t)})},popStep:()=>{let r=o().hardwareStepStack.length-1;if((o().hardwareStepSubStack[r]??[]).length)return e(Ce(s=>{s.hardwareStepSubStack[r]=s.hardwareStepSubStack[r].slice(0,-1)}));e(Ce(s=>{s.hardwareStepStack=s.hardwareStepStack.slice(0,-1)}))},pushSubStep:t=>{let c=o().hardwareStepStack.length-1,s=o().hardwareStepSubStack[c]??[];e(Ce(S=>{S.hardwareStepSubStack[c]=s.concat([t])}))},currentStep:()=>{let t=o().hardwareStepStack,r=o().hardwareStepSubStack,c=t.length>0?t.length-1:t.length;return r[c]?.length?ke(r[c]):ke(t)},setExistingAccounts:t=>{e({existingAccounts:t})},setSelectedChains:(t,r)=>{e({selectedChains:t,selectedChainsMap:r})},setDecrementChainImportStep:()=>{let t=o().chainImportStep;e({chainImportStep:t-1})},setIncrementChainImportStep:()=>{let t=o().chainImportStep;e({chainImportStep:t+1})},setDerivedAccountGroups:t=>{e({derivedAccountGroups:t})},setDiscoveredAccounts:(t,r)=>{e({discoveredAccounts:t,activeAccountsFound:r})},selectAccount:t=>{let c={...o().selectedAccounts};c[t]=!0,e({selectedAccounts:c})},deselectAccount:t=>{let c={...o().selectedAccounts};delete c[t],e({selectedAccounts:c})},setSelectedAccounts:t=>{e({selectedAccounts:t})},setOnConnectHardwareAccounts:t=>{e({onConnectHardwareAccounts:t})},setOnConnectHardwareDone:t=>{e({onConnectHardwareDone:t})}}));A();C();A();C();A();C();var dt=i.main`
  width: ${420}px;
  min-height: ${480}px;
  position: relative;
  overflow: hidden;
  background-color: #222222;
  border: 1px solid #323232;
  border-radius: 16px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
`;var lo=i(dt)`
  display: flex;
  flex-direction: column;
`,ho=i.div`
  display: flex;
  flex-direction: column;
  flex: 1;
  width: 100%;
  padding: 20px 20px;
`,Y=i.div`
  padding-top: 44px;
`,E=i.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
  width: 100%;
  overflow: auto;
`;A();C();var H=Q(R());A();C();var a=Q(R());A();C();var k=Q(R());A();C();var F=Q(R());var xe=()=>{let{t:e}=v(),{discoveredAccounts:o,selectedAccounts:t,onConnectHardwareAccounts:r,onConnectHardwareDone:c}=I(),{mutateAsync:s}=Je(),[S,y]=(0,F.useState)(!1),g=(0,F.useMemo)(()=>o.filter(n=>!!t[n.discoveryIdentifier]),[o,t]);return(0,F.useEffect)(()=>{if(g.length){let n=[],w=new Set;for(let f of g){let{accounts:b,seedIndex:D,accountIndex:T}=f,W=[],L=[];for(let m of b)$e(m.derivationPathType)?(L.push({pathType:m.derivationPathType,value:m.publicKey}),(!("amount"in m)||parseFloat(m.amount)!==0)&&w.add(m.chainType)):(Ke(m.derivationPathType)||Ye(m.derivationPathType))&&W.push({pathType:m.derivationPathType,value:m.address});n.push({derivationIndex:D,addresses:W,publicKeys:L,accountIndex:T})}r({accounts:n}).then(()=>{w.size>0&&s({addressTypes:Array.from(w)})}).finally(()=>y(!0))}else y(!0)},[g,r,s]),F.default.createElement(E,null,F.default.createElement(Y,null,F.default.createElement(K,{icon:F.default.createElement(P,{type:"success"}),primaryText:e("connectHardwareAccountsAddedInterpolated",{numOfAccounts:g.length}),headerStyle:"large",secondaryText:e("connectHardwareFinishSecondaryText")})),F.default.createElement(B,{onClick:c,theme:"primary",disabled:!S},e("pastParticipleDone")))};A();C();var N=Q(R());A();C();var h=Q(R());var kt=(e,o,t)=>{switch(o){case"seed":return e("onboardingImportAccountsAccountName",{walletIndex:t});case"ledger":return e("onboardingImportAccountsLedgerAccountName",{walletIndex:t})}},Dt=({account:e})=>{let{t:o}=v();return h.default.createElement(Mt,null,h.default.createElement(Ot,null,h.default.createElement(ae,{networkID:e.chain.id,size:40,borderColor:"bgRow"})),h.default.createElement(Pt,null,h.default.createElement(Bt,null,h.default.createElement(at,{networkID:e.chain.id,walletAddress:e.address},h.default.createElement(Te,null,e.chain.name)),h.default.createElement(Te,null,Xe(e.address,4))),h.default.createElement(ve,null,"amount"in e&&"chain"in e?h.default.createElement(pt,null,Ve(e.amount)," ",e.chain.symbol):null,"amount"in e?h.default.createElement(pt,null,e.lastActivityTimestamp?o("onboardingImportAccountsLastActive",{formattedTimestamp:Ue(e.lastActivityTimestamp*1e3,!0)}):o("onboardingImportAccountsCreateNew")):null)))},ut=h.default.memo(({accountType:e,accounts:o,checked:t,accountIndex:r,onPress:c})=>{let{t:s}=v(),S=r+1;return h.default.createElement(mt,null,h.default.createElement(Et,null,h.default.createElement(Te,null,kt(s,e,S)),h.default.createElement(me,{checked:t,onChange:c,"data-testid":"account-select-address-row-checkbox"})),o.map((y,g)=>h.default.createElement(Dt,{key:`${y.address}-${g}`,account:y})))}),Fo=h.default.memo(({totalAccounts:e,selectedAccounts:o,onPress:t})=>{let{t:r}=v();return h.default.createElement(mt,null,h.default.createElement(Nt,null,h.default.createElement(Te,null,r("onboardingSelectAccountsNoOfAccountsSelected",{numOfAccounts:o}))," ",h.default.createElement(Lt,null,r("onboardingSelectAccountSelectAllText")," ",h.default.createElement(me,{checked:o===e,onChange:t,"data-testid":"account-select-all-checkbox"}))))}),mt=i.div`
  margin-bottom: 24px;
  width: 100%;
`,Ot=i.div`
  flex-shrink: 0;
  margin-right: 10px;
`,Pt=i.div`
  display: flex;
  flex-direction: column;
  width: 100%;
`,ve=i.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
`,Bt=i(ve)`
  margin-bottom: 2px;
`,Nt=i(ve)`
  background: #2a2a2a;
  margin-bottom: 1px;
  padding: 12px 10px 12px 14px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`,Lt=i.div`
  display: flex;
  align-items: center;
  gap: 10px;
`,Et=i(ve)`
  background: #2a2a2a;
  margin-bottom: 1px;
  padding: 12px 16px 12px 14px;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;

  & > span {
    margin-right: 0;
  }
`,Mt=i.div`
  background: #2a2a2a;
  margin-top: 1px;
  padding: 17px 16px 17px 14px;
  width: 100%;
  display: flex;
  align-items: center;

  &:last-of-type {
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
  }
`,Te=i(_).attrs({size:16,lineHeight:19,weight:600})``,pt=i(_).attrs({size:14,lineHeight:17,weight:400,color:"#777777"})``;var lt=({activeAccounts:e})=>{let{t:o}=v(),{selectedAccounts:t,selectAccount:r,deselectAccount:c,pushSubStep:s}=I(),S=(0,N.useMemo)(()=>Object.values(t).filter(n=>!!n).length===0,[t]),y=(0,N.useCallback)(()=>{s(N.default.createElement(xe,{preventBack:!0}))},[s]);return N.default.createElement(E,null,N.default.createElement("div",{style:{marginBottom:15}},N.default.createElement("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",marginBottom:30}},N.default.createElement(_,{weight:500,size:30,lineHeight:34,maxWidth:"320px"},o("connectHardwareSelectAccounts")),N.default.createElement(Ft,{wordBreak:"break-word",size:18,lineHeight:22,color:"#777777"},o("connectHardwareChooseAccountsToConnect"))),N.default.createElement("div",{style:{maxHeight:420,overflowY:"scroll"}},e.map(({accounts:g,discoveryIdentifier:n,accountIndex:w})=>{let u=!!t[n];return N.default.createElement(ut,{key:n,accountType:"ledger",accounts:g,accountIndex:w,checked:u,onPress:()=>{u?c(n):r(n)}})}))),N.default.createElement(B,{onClick:y,theme:"primary",disabled:S},o("commandContinue")))},Ft=i(_)`
  margin-top: 15px;
`;var ht=()=>{let{t:e}=v(),{discoveredAccounts:o,activeAccountsFound:t,setSelectedAccounts:r,pushSubStep:c}=I(),s=(0,k.useMemo)(()=>{let g;if(t){let n=o.filter(w=>w.status==="undiscovered"||w.isSelectedByDefault);g=e(n.length===1?"connectHardwareFoundAccountsWithActivitySingular":"connectHardwareFoundAccountsWithActivity",{numOfAccounts:n.length})}else g=e("connectHardwareFoundSomeAccounts");return g},[t,e,o]),S=(0,k.useCallback)(()=>{c(k.default.createElement(lt,{activeAccounts:o}))},[c,o]),y=(0,k.useCallback)(()=>{c(k.default.createElement(xe,{preventBack:!0}))},[c]);return(0,k.useEffect)(()=>{let g=o.reduce((n,w,u)=>((w.status==="discovered"&&w.isSelectedByDefault||u===0)&&(n[w.discoveryIdentifier]=!0),n),{});r(g)},[o,r,t,e]),k.default.createElement(E,null,k.default.createElement(Wt,null,k.default.createElement(K,{icon:k.default.createElement(P,{type:"success"}),primaryText:e("connectHardwareConnectAccounts"),headerStyle:"large",secondaryText:s})),k.default.createElement(Gt,{onClick:S,theme:"default"},e("connectHardwareSelectAccounts")),k.default.createElement(B,{onClick:y,theme:"primary"},e("commandContinue")))},Wt=i(Y)`
  margin-bottom: 35px;
`,Gt=i(B)`
  margin-bottom: 10px;
`;var _t=19,jt=e=>{let o=new Set;for(let t of e)for(let{address:r}of t.addresses)o.add(r);return o},le=()=>{let{chainImportStep:e,setIncrementChainImportStep:o,selectedChains:t,selectedChainsMap:r,pushStep:c,pushSubStep:s,setDiscoveredAccounts:S,setDerivedAccountGroups:y}=I(),g=(0,a.useRef)(I.getState().derivedAccountGroups),{t:n,i18n:w}=v(),u=e-1,f=t[u],{data:b=[],isFetched:D,isError:T}=I(p=>p.existingAccounts),[W,L]=(0,a.useState)(!1),m=(0,a.useMemo)(()=>{let p=[],l=r.get(f)||{};for(let[G,X]of Object.entries(l))X&&p.push(G);return[p[0]]},[f,r]),{chainNameTextOr:q,chainNameTextAnd:ee}=(0,a.useMemo)(()=>{let p=m.map(X=>M.getChainName(ye.get(X).ledgerAppOverride??X)),l=new Intl.ListFormat(w.resolvedLanguage,{style:"long",type:"disjunction"}),G=new Intl.ListFormat(w.resolvedLanguage,{style:"long",type:"conjunction"});return{chainNameTextOr:l.format(p),chainNameTextAnd:G.format(p)}},[m,w]),te=(0,a.useMemo)(()=>m.map(p=>{let l=ye.get(p).ledgerAppOverride??p;return a.default.createElement(ae,{key:M.getMainnetNetworkID(ye.get(l).ledgerAppOverride??l),networkID:l,size:72,borderColor:"bgWallet"})}),[m]);(0,a.useEffect)(()=>{let p=I.subscribe(l=>g.current=l.derivedAccountGroups);return()=>p()},[]);let $=(0,a.useMemo)(()=>{let p=[];switch(f){case"solana":{p.push({pathType:"bip44Root"});break}case"eip155":{p.push({pathType:"bip44RootEthereum"});break}case"bip122_p2tr":case"bip122_p2wpkh":case"bip122_p2sh":case"bip122_p2pkh":break}for(let l=0;l<_t;++l)switch(f){case"solana":{p.push({index:l,pathType:"bip44Change"}),p.push({index:l,pathType:"bip44"});break}case"eip155":{p.push({index:l,pathType:"bip44Ethereum"}),p.push({index:l,pathType:"bip44EthereumSecondary"});break}case"bip122_p2tr":case"bip122_p2wpkh":case"bip122_p2sh":case"bip122_p2pkh":{p.push({index:l,pathType:"bitcoinTaproot"},{index:l,pathType:"bitcoinNativeSegwit"});break}}return p},[f]),[se,ie]=(0,a.useState)(!0),{data:oe=Re}=it(se,!0),{data:[He]}=je(["kill-ledger-xpub-derivation"]),{data:Z,error:Be,fetchStatus:gt,refetch:Ne}=st(oe,$,!0,!He),At=gt==="fetching",Ie=!oe.isConnected&&oe.status!=="reconnecting",[Ct,St]=(0,a.useState)(!1),{data:he,refetch:Le}=be(Ct,!0);(0,a.useEffect)(()=>{Ie&&ie(!1)},[Ie]),(0,a.useEffect)(()=>{he?.type==="granted"&&(ie(!0),St(!1))},[he]);let Ee=Qe(),Me=(0,a.useCallback)(async()=>{if(Z&&Object.keys(Z).length){let p=[...g.current],l=0;for(let G of Object.values(Z)){let de={accounts:{...(p[l]??{accounts:{}}).accounts},derivationIndex:$[l].index},fe=M.getChainIDs(G.addressType).filter(ge=>Ee.includes(ge));for(let ge of fe){let pe=M.getNetworkIDs(ge);for(let re of pe)m.includes(re)&&(de.accounts[`${re}-${G.address}`]={chainType:G.addressType,chainId:re,address:G.address,publicKey:G.publicKey,pathParams:$[l]})}p[l]=de,l++}if(y(p),D&&t.length===e){L(!0);let G=jt(b),X=p.reduce((d,O)=>{let ue=!1;for(let{address:We}of Object.values(O.accounts))ue=ue||G.has(We);return ue||d.push(O),d},[]),de=[],fe=[];for(let d=0;d<X.length;d+=De.extension){let O=X.slice(d,d+De.extension).map(ue=>Object.entries(ue.accounts).reduce((Ge,[xt,Tt])=>(Ge[xt]={account:Tt},Ge),{}));fe.push(O)}for(let d of fe)de.push(Ze(d));let pe=(await Promise.all(de)).flat().map(d=>{switch(d.status){case"discovered":return{...d,accounts:d.accounts.filter(O=>O.hasAccountActivity||Ae(O.derivationPathType))};case"undiscovered":return{...d,accounts:d.accounts.filter(O=>Ae(O.derivationPathType))}}}).filter(d=>d.accounts.length>0).map(d=>{let O=_e();return{...d,discoveryIdentifier:O}}),re=pe.filter(d=>d.status==="undiscovered"||d.isSelectedByDefault),wt=pe.filter(d=>!(d.status==="undiscovered"||d.isSelectedByDefault)).slice(0,2),Fe=re.length>0,yt=b.filter(d=>d.type==="ledger").length,bt=(Fe?[...re,...wt]:pe.filter(d=>!d.accounts.some(O=>!Ae(O.derivationPathType))).slice(0,3)).map((d,O)=>({...d,accountIndex:yt+O}));S(bt,Fe),c(a.default.createElement(ht,{preventBack:!0}))}}},[Z,y,D,t.length,e,$,Ee,m,b,S,c]);(0,a.useEffect)(()=>{Z&&Object.keys(Z).length===$.length&&(Me(),t.length!==e&&(o(),s(a.default.createElement(le,{preventBack:!0}))))},[Z,$,c,s,e,t,Me,o]);let j,z,U,J,ne=()=>{};return T?(j=a.default.createElement(P,{type:"failure"}),z=n("connectHardwareErrorLedgerGeneric"),U=n("connectHardwareErrorLedgerPhantomLocked"),ne=async()=>{let p=await ot();p.id!==void 0&&nt(p.id)},J=n("commandClose")):he&&he.type!=="granted"?(j=a.default.createElement(P,{type:"warning"}),z=n("connectHardwarePermissionDeniedPrimary"),U=n("connectHardwarePermissionDeniedSecondary"),J=n("homeErrorButtonText"),ne=Le):Ie?(j=a.default.createElement(P,{type:"warning"}),z=n("connectHardwarePermissionUnableToConnect"),U=n("connectHardwarePermissionUnableToConnectDescription"),J=n("commandConnect"),ne=Le):Be instanceof et?(j=a.default.createElement(P,{type:"failure"}),z=n("connectHardwareErrorLedgerLocked"),U=n("connectHardwareErrorLedgerLockedDescription"),J=n("homeErrorButtonText"),ne=Ne):Be?(j=a.default.createElement(P,{type:"failure"}),z=n("connectHardwareErrorLedgerGeneric"),U=n("connectHardwareErrorLedgerGenericDescription"),J=n("homeErrorButtonText"),ne=Ne):oe.status=="reconnecting"?(j=a.default.createElement(P,{defaultIcon:a.default.createElement(ce,null),type:"default"}),z=n("connectHardwareConnecting"),U=n("connectHardwareConnectingDescription")):W?(j=a.default.createElement(P,{defaultIcon:a.default.createElement(ce,null),type:"default"}),z=n("connectHardwareDiscoveringAccounts"),U=n("connectHardwareDiscoveringAccountsDescription")):At?(j=a.default.createElement(P,{defaultIcon:a.default.createElement(ce,null),type:"default"}),z=n("connectHardwareConnectingAccounts"),U=n("connectHardwareFindingAccountsWithActivity",{chainName:ee})):(j=a.default.createElement(Ut,null,te),z=n("connectHardwareMobileOpenAppSingleChain",{chainName:q}),U=n("connectHardwareOpenAppDescription")),a.default.createElement(E,null,a.default.createElement(Y,null,a.default.createElement(K,{icon:j,primaryText:z,headerStyle:"large",secondaryText:U})),J?a.default.createElement(B,{onClick:ne,theme:"primary"},J):a.default.createElement(zt,null,a.default.createElement(_,{color:"#999999",size:14},n("connectHardwareAccountsStepOfSteps",{stepNum:e,totalSteps:t.length}))))},zt=i.div`
  align-self: center;
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 80px;
  padding: 8px 16px;
  max-width: 150px;
`,Ut=i.div`
  display: flex;
  align-items: center;

  & > *:not(:last-child) {
    margin-right: -12.5px;
  }
`;A();C();var x=Q(R());var ft=()=>{let{t:e}=v(),{pushSubStep:o,selectedChains:t,setSelectedChains:r,selectedChainsMap:c}=I(),s=we(),S=Se(),y=(0,x.useCallback)(u=>{let f=new Map(c),b=M.getAddressTypes(u);for(let T of b){let W=c.get(T),L=W?.[u];f.set(T,{...W,[u]:!L})}let D=S.filter(T=>{let W=f.get(T)||{};return Object.values(W).reduce((m,q)=>q?++m:m,0)>0});r(D,f)},[S,r,c]),g=()=>{o(x.default.createElement(le,{preventBack:!0}))};ct(()=>{let u=new Map;for(let f of S)u.set(f,{});for(let f of s){let b=M.getAddressTypes(f);for(let D of b){let T=u.get(D);u.set(D,{...T,[f]:!1})}}r(t,u)},S.length>0&&s.length>0);let n=(0,x.useMemo)(()=>s.map(u=>{let f=M.getAddressTypes(u),b=!1;for(let D of f)b=c.get(D)?.[u]||b;return x.default.createElement(Vt,{key:u,icon:x.default.createElement(ae,{networkID:u,size:40}),networkID:u,onPressChain:y,isChecked:b})}),[s,c,y]),w=(0,x.useMemo)(()=>{let u=0;for(let f of c.values())u+=Object.values(f).reduce((b,D)=>D?++b:b,0);return u===0},[c]);return x.default.createElement(E,null,x.default.createElement(_,{weight:500,size:28,lineHeight:34},e("connectHardwareSelectChains")),x.default.createElement(Kt,null,n),x.default.createElement(B,{onClick:g,theme:"primary",disabled:w},e("commandContinue")))},Vt=({networkID:e,icon:o,onPressChain:t,isChecked:r})=>x.default.createElement(qt,{onClick:()=>{t(e)}},x.default.createElement(Yt,null,x.default.createElement($t,null,o),x.default.createElement(_,{size:16,weight:600},M.getNetworkName(e))),x.default.createElement(me,{checked:r})),qt=i.div`
  align-items: center;
  background-color: #2a2a2a;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  padding: 16px 24px 16px 12px;

  :last-child {
    margin-bottom: 28px;
  }

  > span {
    margin-right: 0px;
  }
`,$t=i.div`
  margin-right: 12px;
`,Kt=i.div`
  margin-top: 20px;
`,Yt=i.div`
  display: flex;
  align-items: center;
`;var Xt=()=>{ze();let{t:e}=v(),{pushStep:o,setSelectedChains:t}=I(),r=we(),c=Se(),{data:s,isFetching:S,refetch:y}=be(!0,!0),{buttonDisabled:g,defaultIcon:n,primaryText:w,secondaryText:u,buttonText:f,iconType:b,onClick:D}=(0,H.useMemo)(()=>{let T=!1,W=H.default.createElement(ce,null),L,m,q,ee="default",te=qe;if(S)L=e("connectHardwareSearching"),m=e("connectHardwareMakeSureConnected"),q=e("commandContinue"),T=!0;else if(s?.type==="granted"){let $=s.transport.deviceModel?.productName??"Ledger";ee="success",L=e("connectHardwarePairSuccessPrimary",{productName:$}),m=e("connectHardwarePairSuccessSecondary",{productName:$}),q=e("commandContinue"),T=!1,te=()=>{if(c.length===1){let se=new Map;se.set(c[0],{});for(let ie of r){let oe=M.getAddressTypes(ie);for(let He of oe)se.set(He,{[ie]:!0})}t(c,se),o(H.default.createElement(le,{preventBack:!0}))}else o(H.default.createElement(ft,{onBackCallback:()=>{t([],new Map)}}))}}else s?.type==="denied"?(ee="failure",L=e("connectHardwarePermissionDeniedPrimary"),m=e("connectHardwarePermissionDeniedSecondary"),q=e("commandTryAgain"),T=!1,te=y):(!s||s.type==="unable-to-connect")&&(ee="failure",L=e("connectHardwarePermissionUnableToConnect"),m=e("connectHardwareWaitingForApplicationSecondaryText"),q=e("commandTryAgain"),T=!1,te=y);return{buttonDisabled:T,defaultIcon:W,primaryText:L,secondaryText:m,buttonText:q,iconType:ee,onClick:te}},[r,c,s,o,y,S,t,e]);return H.default.createElement(E,null,H.default.createElement(Y,null,H.default.createElement(K,{icon:H.default.createElement(P,{defaultIcon:n,type:b}),primaryText:w,headerStyle:"large",secondaryText:u})),H.default.createElement(B,{onClick:D,theme:"primary",disabled:g},f))},fr=()=>{let{t:e}=v(),{pushSubStep:o}=I(),t=()=>o(H.default.createElement(Xt,null));return H.default.createElement(E,null,H.default.createElement(Y,null,H.default.createElement(K,{icon:H.default.createElement(rt,null),primaryText:e("connectHardwareLedger"),headerStyle:"large",secondaryText:e("connectHardwareStartConnection"),animateText:!0})),H.default.createElement(B,{onClick:t,theme:"primary"},e("commandConnect")))};export{I as a,dt as b,lo as c,ho as d,ut as e,Fo as f,fr as g};
//# sourceMappingURL=chunk-JGDK6WWY.js.map
