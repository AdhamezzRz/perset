import subprocess, sys
FF='ffmpeg'
ENC=['-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r','30','-movflags','+faststart']
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2500:]); sys.exit(1)
# 1 shutter reveal
run([FF,'-y','-loglevel','error','-i','k1.mp4','-framerate','30','-i','fr_s1/f%04d.png','-filter_complex',
 "[0:v]scale=1080:1920:flags=lanczos,fps=30,tpad=start_mode=clone:start_duration=0.85:stop_mode=clone:stop_duration=0.6,trim=duration=6.3,setpts=PTS-STARTPTS[v];[v][1:v]overlay=0:0:shortest=1,format=yuv420p[out]",
 '-map','[out]','-t','6.3']+ENC+['story-1-were-open.mp4'])
# 2 receipt
run([FF,'-y','-loglevel','error','-framerate','30','-i','fr_s2/f%04d.jpg']+ENC+['story-2-the-receipt.mp4'])
# 3 plates
run([FF,'-y','-loglevel','error','-framerate','30','-i','fr_s3/f%04d.jpg']+ENC+['story-3-pick-your-plate.mp4'])
# 4 seat
run([FF,'-y','-loglevel','error','-i','k2.mp4','-framerate','30','-i','fr_s4/f%04d.png','-filter_complex',
 "[0:v]scale=1080:1920:flags=lanczos,fps=30,tpad=stop_mode=clone:stop_duration=1.0,trim=duration=5.9,setpts=PTS-STARTPTS[v];[v][1:v]overlay=0:0:shortest=1,format=yuv420p[out]",
 '-map','[out]','-t','5.9']+ENC+['story-4-saved-you-a-seat.mp4'])
# 5 link card
run([FF,'-y','-loglevel','error','-framerate','30','-i','fr_s5/f%04d.jpg']+ENC+['story-5-set-your-table.mp4'])
# combined preview
segs=['story-1-were-open.mp4','story-2-the-receipt.mp4','story-3-pick-your-plate.mp4','story-4-saved-you-a-seat.mp4','story-5-set-your-table.mp4']
durs=[6.3,8.2,7.0,5.9,5.0]; XF=0.3
inputs=[]; 
for s in segs: inputs+=['-i',s]
fc=''; prev='[0:v]'; off=0
for i in range(1,5):
    off+=durs[i-1]-XF; fc+=f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}];"; prev=f'[x{i}]'
run([FF,'-y','-loglevel','error']+inputs+['-filter_complex',fc.rstrip(';'),'-map',prev]+ENC+['story-preview-all.mp4'])
print('done')
