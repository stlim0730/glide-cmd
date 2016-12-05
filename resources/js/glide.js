var glidePersData = Cookies.getJSON('glidePersData');

$(document).ready(function () {

  // 
  // Persistent-data handler
  // 
  if(typeof glidePersData === 'undefined') {
    // This block should only run on the first page of a project
    console.debug('Set initial glidePersData');

    glidePersData = {};
    Cookies.set('glidePersData', glidePersData);
  }

  var updateglidePersData = function(inputElem) {
    var varName = inputElem.data('glide-name');
    var newVal = inputElem.val();
    glidePersData[varName] = newVal;
    // console.debug('updating glidePersData =>', varName, newVal);

    Cookies.set('glidePersData', glidePersData);
  };
  $('.glide-dynamic-forms').change(function(event){ updateglidePersData($(this)); });
  $('.glide-dynamic-forms').keyup(function(event) { updateglidePersData($(this)); });

  var renderGlideTemplate = function() {
    // TODO: enhance performance?
    // var bodyText = $('body').text();
    // if(!bodyText.indexOf('{{') < 0) return;
    // else console.debug('There is a template to fill out.');
    // alert(bodyText.indexOf('{{'));
    
    var bodySrc = $('body').html();
    for(key in glidePersData) {
      var value = glidePersData[key];
      var re = new RegExp('{{' + '\\s*' + key + '\\s*' + '}}', 'g');
      // bodySrc = bodySrc.replace(re, value);
      $('span')
        .filter(function () {
          return re.test($(this).text());
        })
        .text(value)
    }
  };
  renderGlideTemplate();


  // 
  // Event-bubbling handler
  // - This is to enable (potentially) interactive elembents.
  // - Without this, clicking a textinput will trigger
  // the default click-to-next action.
  // 
  var stopBubbling = function(source) {
    // console.info('stop propagation!', source);
    event.stopPropagation();
  };
  $('.glide-dynamic-forms, a').click(function(event) { stopBubbling(this); });


  // 
  // Entry point
  // 
  $('.click-to-next').click(function(event) {
    // If uncommented, links don't work!
    // event.preventDefault();

    event.stopPropagation();

    var nextPageName = $(this).data('next-page');
    if(nextPageName!=='')
      location.href = './' + nextPageName + '.html';
  });

});
