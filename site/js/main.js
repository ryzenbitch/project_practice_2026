const revealItems = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries)=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
},{threshold:0.12});
revealItems.forEach(item=>observer.observe(item));

for (const row of document.querySelectorAll('.res-row[href="#"]')) {
  row.addEventListener('click', event => event.preventDefault());
}
