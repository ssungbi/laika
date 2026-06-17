import codecs

js_code = """
function showImageModal(src) {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.85)';
    overlay.style.zIndex = '9999';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.cursor = 'zoom-out';
    overlay.onclick = function() { document.body.removeChild(overlay); };
    
    const img = document.createElement('img');
    img.src = src;
    img.style.maxWidth = '90%';
    img.style.maxHeight = '90%';
    img.style.border = '4px solid white';
    img.style.borderRadius = '8px';
    img.style.boxShadow = '0 10px 30px rgba(0,0,0,0.6)';
    img.style.transition = 'transform 0.2s ease-out';
    
    overlay.appendChild(img);
    document.body.appendChild(overlay);
}
"""

with codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'a', 'utf-8') as f:
    f.write(js_code)
    
print("Added showImageModal to script.js")
