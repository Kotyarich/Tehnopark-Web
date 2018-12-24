$(document).ready(function() {

    $('.like').click(function(event){
        event.preventDefault();
        console.log("form submitted!")
        var id = $(this).val();
        if (this.getAttribute('add') == 'true') {
            var val = 1;
        } else {
            var val = -1;
        }

        $.ajax({
            url : "like/", // the endpoint
            type : "POST", // http method
            data : {
                pk : id,
                value : val,
            }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log("success"); // another sanity check
                document.getElementById(id).innerHTML = json.result;
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });


    function getCookie(name)
    {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?

                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         }
    });

})
