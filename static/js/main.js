$(document).ready(function () {
    const webSocket = new WebSocket('ws://' + window.location.host + '/nf/');
    webSocket.onmessage = (message) => {
        const data = JSON.parse(message.data);
        console.log(data);

        $('.toasts-container').append(
            `<div class="toast fade show" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header">
                    <strong class="mr-auto">You got ${data.value === 1? 'like': 'dislike'} to question</strong>
                    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="toast-body">
                    User ${data.user} to "${data.question}"
                </div>
            </div>`
        );
        $('.toast').toast();
    };


    $('.like').click(function (event) {
        let val;
        event.preventDefault();
        const id = $(this).val();
        if (this.getAttribute('add') === 'true') {
            val = 1;
        } else {
            val = -1;
        }

        $.ajax({
            url: "like/", // the endpoint
            type: "POST", // http method
            data: {
                pk: id,
                value: val,
            }, // data sent with the post request
            // handle a successful response
            success: function (json) {
                document.getElementById(id).innerHTML = json.result;
            },
            // handle a non-successful response
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    $('.basicAutoComplete').autoComplete({
        resolver: 'custom',
        formatResult: function (item) {
            return {
                value: item.id,
                text: item.title,
                html: [$('<a>').append(item.title).attr('href', `/question/${item.id}/`)]
            };
        },
        events: {
            search: function (qry, callback) {
                // let's do a custom ajax call
                $.ajax('/search/', {data: {'query': qry}}).done(function (res) {
                    callback(res.results)
                });
            }
        }
    });


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

});
