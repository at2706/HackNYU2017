$(document).ready(function(){
    $("#sidebar-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    $('#nearby').click(function(e) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
                };

                $.ajax({
                    url : "/", // the endpoint
                    type : "POST", // http method
                    data : pos, // data sent with the post request

                    // handle a successful response
                    success : function(json) {
                        $('#post-text').val(''); // remove the value from the input
                        console.log(json); // log the returned json to the console
                        console.log("success"); // another sanity check
                        display = document.getElementById("nearby_display");
                        while (display.firstChild) {
                            display.removeChild(display.firstChild);
                        }

                        for(var i=0; i < json['data'].length; i++) {
                            var hospital = json['data'][i];
                            console.log(hospital);
                            var card = document.createElement("div");
                            card.textContent = hospital.name + hospital.phone_number + hospital.address + hospital.distance;

                            display.appendChild(card);
                        }
                    },

                    // handle a non-successful response
                    error : function(xhr,errmsg,err) {
                        
                    }
                });
            });
        }    
    });
});