(function(){
  // reveal-thumbs.js
  function initThumbs(slides){
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
  }

  // expose helper for inline initialization from template
  window.revealThumbsInit = initThumbs;
})();
