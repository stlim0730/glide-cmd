$(document).ready(function () {
  
  $('.click-to-next').click(function (event) {
    // If uncommented, links don't work!
    // event.preventDefault();

    event.stopPropagation();

    var nextPageName = $(this).data('next-page');
    if(nextPageName!=='')
      location.href = './' + nextPageName + '.html';
  });

});
