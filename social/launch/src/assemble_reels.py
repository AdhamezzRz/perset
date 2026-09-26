import subprocess, sys
FF=open('../ffpath').read().strip()
XF=0.5
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(' '.join(cmd)[:400]); print(r.stderr[-2500:]); sys.exit(1)
ENC=['-c:v','libx264','-preset','medium','-crf','17','-r','30','-pix_fmt','yuv420p']
def card(png,out,d):
    run([FF,'-y','-loglevel','error','-loop','1','-t',str(d),'-i',png,'-vf','format=yuv420p,fps=30']+ENC+[out])
def clip(mp4,ov,out,d=5.0,ov_in=0.5):
    fc=(f"[0:v]scale=1080:1920:flags=lanczos,fps=30,trim=duration={d},setpts=PTS-STARTPTS[v];"
        f"[1:v]format=rgba,fade=t=in:st={ov_in}:d=0.6:alpha=1,fade=t=out:st={d-0.9}:d=0.5:alpha=1[o];[v][o]overlay=0:0:shortest=1,format=yuv420p[out]")
    run([FF,'-y','-loglevel','error','-i',mp4,'-loop','1','-t',str(d),'-i',ov,'-filter_complex',fc,'-map','[out]']+ENC+[out])
def plain(mp4,out,d):
    run([FF,'-y','-loglevel','error','-i',mp4,'-vf',f'scale=1080:1920:flags=lanczos,fps=30,trim=duration={d},setpts=PTS-STARTPTS,format=yuv420p','-t',str(d)]+ENC+[out])
def push(img,out,d,zx,zy,z0=1.0,z1=2.6):
    # fast accelerating zoom into a point (zx,zy in 0..1) of a 1080x1920 image
    n=int(d*30)
    fc=(f"[0:v]scale=2160:3840:flags=lanczos,zoompan=z='{z0}+({z1}-{z0})*pow(on/{n},2.2)':x='iw*{zx}-(iw/zoom)*{zx}':y='ih*{zy}-(ih/zoom)*{zy}':d={n}:s=1080x1920:fps=30,format=yuv420p[out]")
    run([FF,'-y','-loglevel','error','-loop','1','-t',str(d),'-i',img,'-filter_complex',fc,'-map','[out]','-t',str(d)]+ENC+[out])
def concat(segs,durs,out,trans):
    inputs=[]
    for s in segs: inputs+=['-i',s]
    fc=''; prev='[0:v]'; off=0
    for i in range(1,len(segs)):
        tr,td=trans[i-1]; off+=durs[i-1]-td
        fc+=f"{prev}[{i}:v]xfade=transition={tr}:duration={td}:offset={off:.3f}[x{i}];"; prev=f'[x{i}]'
    run([FF,'-y','-loglevel','error']+inputs+['-filter_complex',fc.rstrip(';'),'-map',prev,'-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-r','30','-movflags','+faststart',out])
    print('wrote',out,'dur',round(sum(durs)-sum(t[1] for t in trans),2))

C='../clips/'; F='../frames/'
which=sys.argv[1] if len(sys.argv)>1 else 'all'
if which in ('all','r1'):
    card('r1_card_open.png','s1_0.mp4',2.2)
    push(F+'f_wild_plate.jpg','s1_1.mp4',1.6,0.30,0.30)   # into the left parasol
    clip(C+'l61.mp4','r1_ov_1.png','s1_2.mp4')
    push(F+'f_beads_plate.jpg','s1_3.mp4',1.4,0.50,0.50)  # into the palm
    clip(C+'l62.mp4','r1_ov_2.png','s1_4.mp4')
    push(F+'f_past_plate.jpg','s1_5.mp4',1.4,0.62,0.30)   # into the roses
    clip(C+'l63.mp4','r1_ov_3.png','s1_6.mp4')
    card('card_end.png','s_end.mp4',3.0)
    concat(['s1_0.mp4','s1_1.mp4','s1_2.mp4','s1_3.mp4','s1_4.mp4','s1_5.mp4','s1_6.mp4','s_end.mp4'],
           [2.2,1.6,5,1.4,5,1.4,5,3.0],'reel-01-into-the-plate.mp4',
           [('fade',0.4),('zoomin',0.45),('fade',0.5),('zoomin',0.45),('fade',0.5),('zoomin',0.45),('fade',0.6)])
if which in ('all','r2'):
    card('r2_card_open.png','s2_0.mp4',2.2)
    plain('../stopmotion/table_raw.mp4','s2_1.mp4',14.2)
    card('card_end.png','s_end.mp4',3.0)
    concat(['s2_0.mp4','s2_1.mp4','s_end.mp4'],[2.2,14.2,3.0],'reel-02-table-sets-itself.mp4',[('fade',0.4),('fade',0.6)])
if which in ('all','r3'):
    clip(C+'a42.mp4','r3_ov_1.png','s3_1.mp4',ov_in=0.3)
    clip(C+'a43.mp4','r3_ov_2.png','s3_2.mp4',ov_in=0.3)
    card('r3_card_end.png','s3_end.mp4',3.0)
    concat(['s3_1.mp4','s3_2.mp4','s3_end.mp4'],[5,5,3.0],'reel-03-they-know-youre-looking.mp4',[('fade',0.5),('fade',0.6)])
