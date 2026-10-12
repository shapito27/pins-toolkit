# Icons redrawn by eye from the public article screenshot (no product source used).
pin='<span class="em">&#x1F4CC;</span>'
clap='<span class="em">&#x1F44F;</span>'
repin='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="#2d527c" stroke-width="1.6" stroke-linejoin="round"><rect x="9.5" y="2.5" width="12" height="12" fill="#cee8fa"/><rect x="6" y="6" width="12" height="12" fill="#cee8fa"/><rect x="2.5" y="9.5" width="12" height="12" fill="#f4f6f8"/></svg>'
comment='<svg class="ic" viewBox="0 0 24 24"><path d="M12 3.5c5 0 9 3.4 9 7.6s-4 7.6-9 7.6c-.9 0-1.800-.1-2.600-.3L5 20.800l1-3.500C4.100 15.900 3 13.900 3 11.100 3 6.900 7 3.500 12 3.500z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/><path d="M17.500 5.600c2 1.300 3.500 3.300 3.500 5.500 0 4.200-4 7.600-9 7.600 4.300-1.500 7.300-6.400 5.500-13.100z" fill="#005792"/><circle cx="8.300" cy="11" r="1.100"/><circle cx="12" cy="11" r="1.100"/><circle cx="15.700" cy="11" r="1.100"/></svg>'
share='<svg class="ic" viewBox="0 0 24 24"><path d="M6 12L18 6M6 12l12 6" stroke="#111" stroke-width="2"/><circle cx="6" cy="12" r="3" fill="#2ca9bc" stroke="#111" stroke-width="2"/><circle cx="18" cy="6" r="3" fill="#2ca9bc" stroke="#111" stroke-width="2"/><circle cx="18" cy="18" r="3" fill="#2ca9bc" stroke="#111" stroke-width="2"/></svg>'
cal='<svg class="ic" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2.500" fill="#fff" stroke="#45484c" stroke-width="1.500"/><path d="M3.800 6.500h16.400v3H3.800z" fill="#ffb89a"/><path d="M9 3.300v3M15 3.300v3" stroke="#45484c" stroke-width="1.500" stroke-linecap="round"/><path d="M6.500 13h11M6.500 16.800h6M15 16.800h2.500" stroke="#33cc99" stroke-width="1.800" stroke-linecap="round"/></svg>'
down='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.800" stroke-linejoin="round" stroke-linecap="round"><path d="M10 3h4v7l2.500-2 2 2.300L12 16 5.500 10.300l2-2.300L10 10z" fill="#2ca9bc"/><path d="M4 17v4h16v-4"/></svg>'
book='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.400"><path d="M5 2.500h14V21.500l-7-5.300-7 5.300z"/></svg>'
mag='<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="#2c3e50" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M16.500 16.500L21 21"/></svg>'
def card(cls,v):
    rows=''.join(f'<div class="si">{i}<span>{x}</span></div>' for i,x in zip([pin,repin,comment,share,clap,cal],v))
    return f'<div class="card {cls}"><div class="ps">{rows}<div class="si act">{down}{book}{mag}</div></div></div>'
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1808px;height:1736px;background:#fff;overflow:hidden;font-family:-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#111}}
.grid{{display:flex;gap:56px;padding:60px 60px 0}}
.card{{position:relative;flex:1;height:1700px;border-radius:96px 96px 0 0;overflow:hidden}}
.c1{{background:linear-gradient(165deg,#b9ad93 0%,#8d9a78 50%,#55684f 100%)}}
.c2{{background:linear-gradient(195deg,#e3c6a8 0%,#c78e6a 55%,#86563f 100%)}}
.ps{{position:absolute;top:250px;left:0;background:rgb(255 255 255 / 82%);padding:34px 48px 34px 34px;font-size:92px;line-height:1}}
.si{{display:flex;align-items:center;gap:28px;height:180px;white-space:nowrap}}
.ic{{width:120px;height:120px;flex:none}}
.em{{width:120px;flex:none;font-family:"Noto Color Emoji";font-size:100px;line-height:120px;text-align:center}}
.act{{gap:52px}}
</style></head><body><div class="grid">
{card('c1',['29,429','571','17','52','1,981','1 M'])}
{card('c2',['16,947','545','4','15','1,041','1 Y'])}
</div></body></html>'''
open('mock6c.html','w',encoding='utf8').write(html)
