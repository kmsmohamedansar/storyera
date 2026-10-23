#!/usr/bin/env python3
"""Render original docs illustrations as matching SVG/PNG. Optional: Pillow."""
from pathlib import Path
from html import escape
import argparse
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
INK='#182C35'; PAPER='#F6F2E9'; MUTED='#52656C'; GOLD='#D2A65B'; TEAL='#267C72'


def font_path(bold=False):
    candidates = (['/System/Library/Fonts/Supplemental/Arial Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if bold else ['/System/Library/Fonts/Supplemental/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for p in candidates:
        if Path(p).exists(): return p
    raise RuntimeError('Install Arial or DejaVu Sans to regenerate images.')


class Canvas:
    def __init__(self, name, height, title, background=PAPER):
        self.name=name; self.width=1600; self.height=height
        self.im=Image.new('RGB',(self.width,height),background); self.d=ImageDraw.Draw(self.im)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{height}" viewBox="0 0 1600 {height}" role="img"><title>{escape(title)}</title>',f'<rect width="1600" height="{height}" fill="{background}"/>']
    def rect(self,x,y,w,h,fill,r=0,outline=None):
        self.d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=outline,width=2)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{outline}" stroke-width="2"' if outline else '')+'/>')
    def line(self,points,fill=INK,width=3):
        self.d.line(points,fill=fill,width=width)
        self.svg.append(f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{fill}" stroke-width="{width}"/>')
    def text(self,x,y,text,size=28,fill=INK,bold=False):
        font=ImageFont.truetype(font_path(bold),size)
        box=self.d.textbbox((0,0),text,font=font)
        if x+box[2]>self.width-36 or y+box[3]>self.height-16:
            raise ValueError(f'Text overflows {self.name}: {text}')
        self.d.text((x,y),text,font=font,fill=fill,anchor='lt')
        self.svg.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" font-family="Arial, DejaVu Sans, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{fill}">{escape(text)}</text>')
    def arrow(self,x,y,w=40):
        self.line([(x,y),(x+w,y)],TEAL,4)
        self.line([(x+w-12,y-9),(x+w,y),(x+w-12,y+9)],TEAL,4)
    def save(self):
        out=ROOT/'docs/assets';out.mkdir(parents=True,exist_ok=True)
        self.im.save(out/(self.name+'.png'))
        (out/(self.name+'.svg')).write_text('\n'.join(self.svg+['</svg>'])+'\n')


def render():
    c=Canvas('banner',560,'StoryEra: continuity notes with receipts',INK)
    c.text(80,62,'AN AGENT SKILL FOR NOVEL CONTINUITY',22,GOLD,True)
    c.text(76,132,'StoryEra',100,PAPER,True)
    c.text(82,274,'Your story. Your era.',46,PAPER)
    c.text(82,336,'Catch the contradiction.',46,PAPER)
    c.text(83,462,'CITED FACTS   /   CLEAR CLASSIFICATIONS   /   AUTHOR CONTROL',19,GOLD,True)
    # A book and a connected ledger, drawn as original graphics.
    c.rect(1120,110,300,340,'#243E47',14)
    c.rect(1150,140,240,280,PAPER,8)
    c.line([(1270,140),(1270,420)],GOLD,3)
    for y in range(174,370,37):
        c.line([(1172,y),(1248,y)],MUTED,3);c.line([(1290,y),(1368,y)],MUTED,3)
    c.rect(1355,335,116,112,TEAL,16)
    c.line([(1380,387),(1403,412),(1446,365)],PAPER,8)
    c.save()
    c=Canvas('classifications',620,'Four continuity audit outcomes')
    c.text(65,45,'Not every difference is an error.',48,bold=True)
    data=[('01','Contradiction','Incompatible claims.','Cite both. Propose a repair.','#A44F45'),('02','Explained change','A transition is supplied.','Preserve the explanation.',TEAL),('03','Intentional mystery','Concealment is signaled.','Track clues and resolution.','#70668D'),('04','Author question','More than one reading fits.','Ask for a canon decision.','#8A692F')]
    for i,(num,title,a,b,color) in enumerate(data):
        x=65+(i%2)*755;y=145+(i//2)*215
        c.rect(x,y,715,180,'#FFFFFF',16)
        c.rect(x,y,8,180,color,3)
        c.text(x+30,y+25,num,22,color,True); c.text(x+87,y+22,title,32,bold=True)
        c.text(x+30,y+82,a,26,MUTED);c.text(x+30,y+126,b,25,MUTED)
    c.save()
    c=Canvas('workflow',470,'The StoryEra audit workflow')
    c.text(65,42,'From chapter text to reviewable notes.',46,bold=True)
    data=[('01','Scope','Order + hashes'),('02','Read','Full passages'),('03','Ledger','Facts + citations'),('04','Reconcile','Later evidence'),('05','Report','Labels + repairs')]
    for i,(num,title,sub) in enumerate(data):
        x=65+i*302
        c.rect(x,155,270,180,'#FFFFFF',14)
        c.text(x+22,178,num,22,TEAL,True);c.text(x+22,222,title,34,bold=True);c.text(x+22,280,sub,22,MUTED)
        if i<4:c.arrow(x+276,245,20)
    c.text(65,385,'The author decides what becomes canon. The manuscript stays unchanged.',25,MUTED)
    c.save()
    c=Canvas('yakuza-counts',660,'YAKUZA continuity example: keep the two child cohorts separate')
    c.text(65,40,'Two cohorts. One mistaken subtraction.',46,bold=True)
    c.text(65,108,'YAKUZA / VOLUMES ONE–THREE / SPOILER EXAMPLE',20,MUTED,True)
    for x,num,label,sub in [(65,'34','ALREADY SHIPPED','Earlier ledger / still missing'),(825,'14','NEWLY RESCUED','The next shipment / now safe')]:
        c.rect(x,170,710,260,'#FFFFFF',16)
        c.text(x+32,194,num,100,TEAL,True);c.text(x+215,221,label,27,bold=True)
        c.text(x+32,359,sub,26,MUTED)
    c.rect(65,470,1470,120,INK,14)
    c.text(95,497,'48 accounted for = 34 missing + 14 rescued',39,PAPER,True)
    c.text(95,550,'Unless the text explicitly establishes overlap between the groups.',22,GOLD)
    c.save()
    print('Rendered four diagrams with matching SVG sources.')


if __name__=='__main__':
    argparse.ArgumentParser(description=__doc__).parse_args();render()
