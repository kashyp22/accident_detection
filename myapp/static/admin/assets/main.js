/* main.js - Accident Detection using AI (template)
   Wire your AI API/model where marked with TODO comments.
*/

const els = {
  uploadBtn: document.getElementById('btn-upload'),
  liveBtn: document.getElementById('btn-live'),
  fileInput: document.getElementById('file-input'),
  previewVideo: document.getElementById('preview-video'),
  overlayCanvas: document.getElementById('overlay-canvas'),
  demoVideo: document.getElementById('demo-video'),
  demoCanvas: document.getElementById('demo-canvas'),
  log: document.getElementById('log'),
  conf: document.getElementById('conf'),
  confValue: document.getElementById('conf-value'),
  iou: document.getElementById('iou'),
  iouValue: document.getElementById('iou-value'),
  statTime: document.getElementById('stat-time'),
  statCoverage: document.getElementById('stat-coverage'),
  statAccuracy: document.getElementById('stat-accuracy'),
};

function init(){
  if(els.uploadBtn) els.uploadBtn.addEventListener('click',()=> els.fileInput.click());
  if(els.fileInput) els.fileInput.addEventListener('change', handleFileSelect);

  // Settings UI
  syncSettings();
  ['input','change'].forEach(evt => {
    els.conf?.addEventListener(evt, syncSettings);
    els.iou?.addEventListener(evt, syncSettings);
  });

  // Mock stats
  animateStats();
}

function syncSettings(){
  if(els.conf && els.confValue) els.confValue.textContent = Number(els.conf.value).toFixed(2);
  if(els.iou && els.iouValue) els.iouValue.textContent = Number(els.iou.value).toFixed(2);
}

async function handleFileSelect(e){
  const file = e.target.files?.[0];
  if(!file) return;

  const url = URL.createObjectURL(file);
  if(els.previewVideo){ els.previewVideo.src = url; els.previewVideo.muted = true; els.previewVideo.play(); }
  if(els.demoVideo){ els.demoVideo.src = url; }

  // Start mock inference draw loop over previewCanvas
  startMockDetections(els.previewVideo, els.overlayCanvas);
  startMockDetections(els.demoVideo, els.demoCanvas);
}

function logEvent(text){
  if(!els.log) return;
  const li = document.createElement('li');
  li.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
  els.log.prepend(li);
}

/* TODO: Replace this with your actual model/API calls.
   Example sketch:
   - Send frames to /infer endpoint
   - Receive detections: [{x,y,w,h,score,label}]
   - Draw boxes on canvas
*/
let mockIntervals = [];
function startMockDetections(video, canvas){
  if(!video || !canvas) return;
  stopMockDetections(canvas);

  const ctx = canvas.getContext('2d');
  const draw = () => {
    // Resize canvas to match video
    if(video.videoWidth && video.videoHeight){
      canvas.width = video.clientWidth || video.videoWidth;
      canvas.height = video.clientHeight || video.videoHeight;
    }
    ctx.clearRect(0,0,canvas.width,canvas.height);

    // Randomly draw a box as a mock accident every ~1.5s
    if(Math.random() < 0.04){
      const w = 80 + Math.random()*140;
      const h = 40 + Math.random()*90;
      const x = Math.random()*(canvas.width - w);
      const y = Math.random()*(canvas.height - h);
      const score = 0.6 + Math.random()*0.35;
      drawBox(ctx, x, y, w, h, score, 'accident');
      logEvent(`accident @ (${x|0},${y|0}) score=${score.toFixed(2)}`);
    }
  };
  const id = setInterval(draw, 40); // ~25 fps canvas refresh
  mockIntervals.push({canvas, id});
}

function stopMockDetections(canvas){
  mockIntervals = mockIntervals.filter(item => {
    if(item.canvas === canvas){ clearInterval(item.id); return false; }
    return true;
  });
}

function drawBox(ctx, x, y, w, h, score, label){
  ctx.save();
  ctx.lineWidth = 3;
  ctx.strokeStyle = 'rgba(255,93,115,0.95)';
  ctx.fillStyle = 'rgba(255,93,115,0.15)';
  roundRect(ctx, x, y, w, h, 8);
  ctx.fill();
  ctx.stroke();

  const tag = `${label} ${(score*100).toFixed(0)}%`;
  ctx.fillStyle = '#0b1430';
  ctx.strokeStyle = '#ff5d73';
  ctx.lineWidth = 2;
  const pad = 6;
  const tw = ctx.measureText(tag).width + pad*2;
  const th = 20;
  ctx.beginPath();
  ctx.roundRect?.(x, y - th - 6, tw, th, 6);
  ctx.fillStyle = '#ff5d73';
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = '#0b1430';
  ctx.font = '12px Inter, sans-serif';
  ctx.fillText(tag, x + pad, y - 10);
  ctx.restore();
}

function roundRect(ctx, x, y, w, h, r){
  ctx.beginPath();
  ctx.moveTo(x+r, y);
  ctx.lineTo(x+w-r, y);
  ctx.quadraticCurveTo(x+w, y, x+w, y+r);
  ctx.lineTo(x+w, y+h-r);
  ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
  ctx.lineTo(x+r, y+h);
  ctx.quadraticCurveTo(x, y+h, x, y+h-r);
  ctx.lineTo(x, y+r);
  ctx.quadraticCurveTo(x, y, x+r, y);
  ctx.closePath();
}

function animateStats(){
  // Simple playful numbers; replace with real metrics later
  const target = { time: 7.5, coverage: 120, acc: 92 };
  const start = performance.now();
  const dur = 1200;
  const step = (t)=>{
    const p = Math.min(1,(t-start)/dur);
    if(els.statTime) els.statTime.textContent = `${(target.time*p).toFixed(1)} min`;
    if(els.statCoverage) els.statCoverage.textContent = `${Math.round(target.coverage*p)}+`;
    if(els.statAccuracy) els.statAccuracy.textContent = `${Math.round(target.acc*p)}%`;
    if(p<1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// Example integration sketch
/*
async function runInferenceOnFrame(bitmap){
  const body = await blobFromBitmap(bitmap);
  const res = await fetch('/infer', { method: 'POST', body, headers: { 'x-conf': els.conf.value, 'x-iou': els.iou.value }});
  const detections = await res.json(); // [{x,y,w,h,score,label}]
  return detections;
}
*/

window.addEventListener('DOMContentLoaded', init);
