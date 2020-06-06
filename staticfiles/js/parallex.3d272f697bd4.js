$(window).on('scroll', scrollDown);
$('a.btn-fire').on('click', function(e){funClick(e)});

function funClick(e){
   e.preventDefault();
}

function scrollDown(){
    offset = window.pageYOffset;
    let parallex = document.querySelector('.header');
    parallex.style.backgroundPositionY = offset*0.7 + 'px';
}
