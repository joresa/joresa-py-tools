(function(){
  function detectTablesFromText(txt){
    const out = [];
    if(!txt) return out;
    const insertRe = /INSERT\s+INTO\s+[`\"]?(\w+)[`\"]?/ig;
    const createRe = /CREATE\s+TABLE\s+[`\"]?(\w+)[`\"]?/ig;
    let m;
    while((m = insertRe.exec(txt)) !== null){ out.push(m[1]); }
    while((m = createRe.exec(txt)) !== null){ out.push(m[1]); }
    return Array.from(new Set(out));
  }

  function renderTableList(container, tables){
    container.innerHTML = '';
    if(!tables || tables.length===0){ container.innerHTML = '<em class="text-muted">No tables detected</em>'; return; }
    tables.forEach(function(t){
      const div = document.createElement('div'); div.className='table-item';
      div.innerHTML = `<input type="checkbox" value="${t}" checked> <div class="flex-fill" title="${t}">${t}</div>`;
      container.appendChild(div);
    });
  }

  const fa = document.getElementById('file-a-input');
  const fb = document.getElementById('file-b-input');
  const ta = document.querySelector('.js-tables-a');
  const tb = document.querySelector('.js-tables-b');
  const fileAName = document.querySelector('.js-file-a-name');
  const fileBName = document.querySelector('.js-file-b-name');

  function readFileText(file){
    return new Promise(function(resolve,reject){ const r=new FileReader(); r.onload=function(){resolve(r.result||'');}; r.onerror=function(){reject();}; r.readAsText(file); });
  }

  // helper to set visible name and tooltip
  function setFileNameDisplay(elem, file){
    if(!elem) return;
    if(!file){ elem.textContent = 'No file selected'; elem.title = ''; return; }
    elem.textContent = file.name;
    elem.title = file.name;
  }

  fa && fa.addEventListener('change', function(e){ if(fa.files.length){ setFileNameDisplay(fileAName, fa.files[0]); } else { setFileNameDisplay(fileAName, null); } });
  fb && fb.addEventListener('change', function(e){ if(fb.files.length){ setFileNameDisplay(fileBName, fb.files[0]); } else { setFileNameDisplay(fileBName, null); } });

  document.querySelector('#start-compare').addEventListener('click', function(){
    // collect files
    const fileInputA = document.getElementById('file-a-input');
    const fileInputB = document.getElementById('file-b-input');
    if(!fileInputA || !fileInputB || !fileInputA.files.length || !fileInputB.files.length){
      alert('Please select both Source A and Source B .sql files before comparing.');
      return;
    }

    const fileA = fileInputA.files[0];
    const fileB = fileInputB.files[0];

    // collect selected tables
    const tables = [];
    document.querySelectorAll('.js-tables-a .table-item input:checked, .js-tables-b .table-item input:checked')
      .forEach(function(ch){ if(!tables.includes(ch.value)) tables.push(ch.value); });

    // Build FormData for server POST
    const fd = new FormData();
    fd.append('file_a', fileA);
    fd.append('file_b', fileB);
    // append tables as repeated fields
    tables.forEach(function(t){ fd.append('tables', t); });

    const btn = document.getElementById('start-compare');
    const orig = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Comparing...';

    fetch('/tools/wp-db-compare/compare', { method: 'POST', body: fd, credentials: 'same-origin' })
      .then(function(resp){
        // If server redirected to a result page, follow it by setting window.location
        // fetch follows redirects automatically; use resp.url
        if(resp.ok || resp.type === 'cors' || resp.type === 'basic' || resp.redirected){
          // resp.url should be the final URL after redirects
          if(resp.url && resp.url.indexOf('/wp-db-compare/result') !== -1){
            window.location = resp.url;
            return;
          }
        }
        // try to parse json for errors or fall back to text
        return resp.json().then(function(j){ throw new Error((j && j.message) ? j.message : JSON.stringify(j)); }).catch(function(){ return resp.text().then(function(t){ throw new Error(t || 'Compare request failed'); }); });
      })
      .catch(function(err){
        console.error('compare error', err);
        alert('Compare failed: ' + (err && err.message ? err.message : 'unknown error'));
      })
      .finally(function(){ btn.disabled = false; btn.innerHTML = orig; });
  });

  document.querySelectorAll('.js-select-all').forEach(function(btn){ btn.addEventListener('click', function(){ const body = btn.closest('.panel-body').querySelector('.table-list-body'); body.querySelectorAll('.table-item input').forEach(function(i){ i.checked=true; }); }); });
  document.querySelectorAll('.js-deselect-all').forEach(function(btn){ btn.addEventListener('click', function(){ const body = btn.closest('.panel-body').querySelector('.table-list-body'); body.querySelectorAll('.table-item input').forEach(function(i){ i.checked=false; }); }); });

  // Validate button triggers a local "refresh/detect": show spinner, read file and re-run client-side detection
  document.querySelectorAll('.js-validate').forEach(function(btn){ btn.addEventListener('click', function(){
      const panel = btn.closest('.panel');
      const body = panel.querySelector('.table-list-body');
      const input = panel.querySelector('input[type=file]');
      if(!input || !input.files || !input.files.length){ alert('No file selected. Please choose a .sql file first.'); return; }
      const file = input.files[0];
      // quick local extension hint but allow proceeding if user wants
      if(!file.name.toLowerCase().endsWith('.sql')){
        if(!confirm('Selected file does not have a .sql extension. Continue detection?')) return;
      }

      btn.disabled = true; const orig = btn.innerHTML; btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Refreshing...';
      // read file and re-detect tables locally
      readFileText(file).then(function(txt){
        const detected = detectTablesFromText(txt);
        renderTableList(body, detected);
        // update file-info display
        const fileInfo = panel.querySelector('.file-info'); if(fileInfo){ fileInfo.textContent = file.name; fileInfo.title = file.name; }
        // transient success note
        const note = document.createElement('div'); note.className='alert alert-success mt-2 py-1'; note.textContent = 'Tables refreshed';
        try{ panel.querySelector('.panel-body').insertBefore(note, panel.querySelector('.table-list')); }catch(e){}
        setTimeout(()=>{ try{ note.remove(); }catch(e){} }, 2500);
      }).catch(function(){ alert('Could not read file for detection'); }).finally(function(){ btn.disabled = false; btn.innerHTML = orig; });
  }); });
  
  document.getElementById('file-a-input').addEventListener('change', function(){ if(this.files.length){ readFileText(this.files[0]).then(function(txt){ const detected = detectTablesFromText(txt); renderTableList(ta, detected); }).catch(function(){ console.error('read error a'); }); } });
  document.getElementById('file-b-input').addEventListener('change', function(){ if(this.files.length){ readFileText(this.files[0]).then(function(txt){ const detected = detectTablesFromText(txt); renderTableList(tb, detected); }).catch(function(){ console.error('read error b'); }); } });

})();
