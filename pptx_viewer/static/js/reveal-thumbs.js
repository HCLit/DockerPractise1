(function(){
  // reveal-thumbs.js
  function initThumbs(slides, showDefault = true){
    const container = document.getElementById('thumbs');
    if(!container) return;

    container.innerHTML = '';
    slides.forEach((s, i) => {
      const img = document.createElement('img');
      img.src = '/slides/' + s.img;
      img.dataset.index = i;
      img.alt = 'Slide ' + s.index;
      img.addEventListener('click', ()=>{
        Reveal.slide(i);
      });
      container.appendChild(img);
    });

    // visibility state
    let visible = !!showDefault;
    function setVisible(v){
      visible = !!v;
      container.style.display = visible ? '' : 'none';
      // update aria state
      const btn = document.getElementById('toggle-thumbs');
      if(btn){ btn.setAttribute('aria-pressed', visible ? 'true' : 'false'); btn.textContent = visible ? 'Hide Thumbnails' : 'Show Thumbnails'; }
    }

    function setActive(index){
      const imgs = container.querySelectorAll('img');
      imgs.forEach(el => el.classList.toggle('active', Number(el.dataset.index) === index));
      const active = container.querySelector('img.active');
      if(active) active.scrollIntoView({behavior:'smooth', inline:'center'});
    }

    Reveal.on('slidechanged', e=>{
      setActive(e.indexh);
    });

    Reveal.on('ready', e=>{
      setActive(Reveal.getIndices().h || 0);
    });

    // initialize visibility
    setVisible(showDefault);

    // expose toggle function that returns the new state
    window.toggleRevealThumbs = function(){
      setVisible(!visible);
      try{ localStorage.setItem('reveal_thumbs', visible ? '1' : '0'); }catch(e){}
      return visible;
    };

    // expose a getter
    window.isRevealThumbsVisible = function(){ return visible; };
  }

  // expose helper for inline initialization from template
  window.revealThumbsInit = initThumbs;
})();
