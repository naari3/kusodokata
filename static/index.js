$(function () {
  $('body:first').fadeIn('slow');
  $('.back:first').foggy({
    blurRadius: 10,
    opacity: 1,
    cssFilterSupport: true
  });
})
