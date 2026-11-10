#!/bin/bash
# usage: shot.sh step [WxH]   (any script error is printed on the page and still marks it ready)
P=$(cd "$(dirname "$0")" && pwd)
s=$1; vp=${2:-1920x1080}
mkdir -p $P/t/$s
cat > $P/t/$s/head.html <<EOF
<script>
history.replaceState(null,'','#$s'); window.__noPrecompile = true;
const E=(m)=>{document.documentElement.dataset.ready=1;setTimeout(()=>{const p=document.createElement('pre');p.style.cssText='position:fixed;top:0;left:0;z-index:99;color:red;background:#fff;font-size:18px;white-space:pre-wrap';p.textContent=m;document.body.appendChild(p);},0)};
addEventListener('error',e=>E(e.message+' '+(e.error&&e.error.stack)));
addEventListener('unhandledrejection',e=>E(String(e.reason&&e.reason.stack||e.reason)));
</script>
EOF
{ cat $P/t/$s/head.html; cat "$P/AEP0.2 presentation.html"; } > $P/t/$s/index.html
rm $P/t/$s/head.html
timeout 150 vibe-shot $P/t/$s --viewport $vp --wait-for 'html[data-ready]' --out $P/t/$s.png 2>&1 | grep -v identity | tail -1
