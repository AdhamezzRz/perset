import subprocess, sys, os
FF=open('../ffpath').read().strip()
CLIP_D=5.0; CARD_D=2.4; XF=0.6
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
def seg_card(png,out,d=CARD_D):
    run([FF,'-y','-loglevel','error','-loop','1','-t',str(d),'-i',png,'-vf','format=yuv420p,fps=30','-c:v','libx264','-preset','medium','-crf','17','-r','30',out])
def seg_clip(mp4,ov,out,d=CLIP_D,ov_in=0.7,ov_out=0.6):
    vf=(f"[0:v]scale=1080:1920:flags=lanczos,fps=30,trim=duration={d},setpts=PTS-STARTPTS[v];"
        f"[1:v]format=rgba,fade=t=in:st={ov_in}:d=0.7:alpha=1,fade=t=out:st={d-ov_out-0.5}:d=0.5:alpha=1[o];"
        f"[v][o]overlay=0:0:shortest=1,format=yuv420p[out]")
    run([FF,'-y','-loglevel','error','-i',mp4,'-loop','1','-t',str(d),'-i',ov,'-filter_complex',vf,'-map','[out]','-c:v','libx264','-preset','medium','-crf','17','-r','30',out])
def concat(segs,durs,out):
    inputs=[]; 
    for s in segs: inputs+=['-i',s]
    fc=''; prev='[0:v]'; off=0
    for i in range(1,len(segs)):
        off += durs[i-1]-XF
        fc+=f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}];"; prev=f'[x{i}]'
    fc=fc.rstrip(';')
    run([FF,'-y','-loglevel','error']+inputs+['-filter_complex',fc,'-map',prev,'-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-r','30','-movflags','+faststart',out])
    print('wrote',out, 'expected duration', sum(durs)-XF*(len(segs)-1))

C='../clips/'
# Reel 1 — Beautiful per piece
seg_card('card_open_r1.png','s_r1_0.mp4')
seg_clip(C+'c1.mp4','ov_r1_1.png','s_r1_1.mp4')
seg_clip(C+'c2.mp4','ov_r1_2.png','s_r1_2.mp4')
seg_clip(C+'c3.mp4','ov_r1_3.png','s_r1_3.mp4')
seg_card('card_end.png','s_end.mp4',3.0)
concat(['s_r1_0.mp4','s_r1_1.mp4','s_r1_2.mp4','s_r1_3.mp4','s_end.mp4'],[CARD_D,5,5,5,3.0],'reel-01-per-piece.mp4')
# Reel 2 — Inside the set
seg_card('card_open_r2.png','s_r2_0.mp4')
seg_clip(C+'c4.mp4','ov_r2_1.png','s_r2_1.mp4')
seg_clip(C+'c5.mp4','ov_r2_2.png','s_r2_2.mp4',ov_in=0.5,ov_out=0.4)
concat(['s_r2_0.mp4','s_r2_1.mp4','s_r2_2.mp4','s_end.mp4'],[CARD_D,5,5,3.0],'reel-02-inside-the-set.mp4')
# Reel 3 — Three stories
seg_card('card_open_r3.png','s_r3_0.mp4')
seg_clip(C+'c6.mp4','ov_r3_1.png','s_r3_1.mp4')
seg_clip(C+'c7.mp4','ov_r3_2.png','s_r3_2.mp4')
seg_clip(C+'c8.mp4','ov_r3_3.png','s_r3_3.mp4')
seg_card('card_end_r3.png','s_end_r3.mp4',3.2)
concat(['s_r3_0.mp4','s_r3_1.mp4','s_r3_2.mp4','s_r3_3.mp4','s_end_r3.mp4'],[CARD_D,5,5,5,3.2],'reel-03-three-stories.mp4')
