$(function () {
    $('[data-toggle="popover"]').popover();
});

$('.clock-form').submit(function() {
    $('.overlay').show();
});

$("#skill-filter").on("change", function() {
    var value = $("#skill-filter option:selected").text();
    value = value.substr(0, value.indexOf('(')-1);
    $(".card").filter(function() {
      $(this).toggle($(this).text().toLowerCase().replace(/(\r\n|\n|\r)/gm,"").indexOf(value.toLowerCase()) > -1)
    });
});

$("#company-filter").on("change", function() {
    var value = $("#company-filter option:selected").text();
    value = value.substr(0, value.indexOf('(')-1);
    $(".card").filter(function() {
      $(this).toggle($(this).text().toLowerCase().replace(/(\r\n|\n|\r)/gm,"").indexOf(value.toLowerCase()) > -1)
    });
});

$(".project_status_select").on("change", function() {
    str = String(location);
    root = str.substr(0, str.lastIndexOf("/"));
    endpoint = root + '/project/status/' + $(this).attr('data-project') + '/' + $(this).val();
    // alert(endpoint);
    location = endpoint;
});

$('[data-toggle=confirmation]').confirmation();
$('[data-toggle=confirmation-singleton]').confirmation({ singleton: true });
$('[data-toggle=confirmation-popout]').confirmation({ popout: true });

$('[data-toggle=confirmation-custom]').confirmation({
title: 'Approve item ?',
content: 'An email will be sent to the item owner.',
buttons: [
  {
    label: 'Approved',
    class: 'btn btn-xs btn-success',
    icon: 'glyphicon glyphicon-ok'
  },
  {
    label: 'Rejected',
    class: 'btn btn-xs btn-danger',
    icon: 'glyphicon glyphicon-remove'
  },
  {
    label: 'Need review',
    class: 'btn btn-xs btn-warning',
    icon: 'glyphicon glyphicon-search'
  },
  {
    label: 'Decide later',
    class: 'btn btn-xs btn-default',
    icon: 'glyphicon glyphicon-time'
  }
]


});

/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("help").style.width = "350px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("help").style.width = "0";
}

/* Copy to clipboard : https://www.w3schools.com/howto/howto_js_copy_clipboard.asp */
function copy_email_address() {
    var email = document.querySelector('#email-address');
    email.select();
    document.execCommand("copy");

    var node = document.createElement('DIV');
    node.id = 'toast-99';
    node.className = 'toast show toast-message';
    var textnode = document.createTextNode('Email address copied to clipboard');
    node.appendChild(textnode);
    document.getElementById("logo").appendChild(node);

    setTimeout(function(){
        var toast = document.querySelector('#toast-99');
        toast.parentNode.removeChild(toast);
        }, 3000);

    // <div id="toast-1" class="toast toast-error " role="alert">
    //             Invalid email or password
    //         </div>
}

